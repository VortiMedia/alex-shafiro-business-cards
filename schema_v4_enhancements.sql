-- =====================================================
-- Business Card Generator v4.0 - Schema Enhancements
-- Quick Wins Implementation
-- =====================================================

-- Add version tracking
CREATE TABLE IF NOT EXISTS schema_migrations (
  version INTEGER PRIMARY KEY,
  applied_at TIMESTAMPTZ DEFAULT NOW(),
  description TEXT,
  applied_by TEXT DEFAULT CURRENT_USER
);

-- Record this enhancement version
INSERT INTO schema_migrations (version, description) 
VALUES (2, 'Quick wins: composite indexes, cost prediction, session timeouts, conversion funnel')
ON CONFLICT (version) DO NOTHING;

-- =====================================================
-- 1. COMPOSITE INDEXES FOR BETTER PERFORMANCE
-- =====================================================

-- Session lookup with status and phase (common query pattern)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_design_sessions_user_status_phase 
ON design_sessions(user_id, status, current_phase);

-- Cost tracking by model and time (for analytics)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_api_usage_model_time_cost 
ON api_usage_log(ai_model, created_at DESC, cost);

-- Iteration chain traversal (parent -> child relationships)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_design_iterations_parent_phase_order 
ON design_iterations(parent_concept_id, phase, iteration_order) 
WHERE parent_concept_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_design_iterations_parent_iter_phase_order 
ON design_iterations(parent_iteration_id, phase, iteration_order) 
WHERE parent_iteration_id IS NOT NULL;

-- User journey analysis (selections by session and phase)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_selections_session_phase_created 
ON user_selections(session_id, phase, created_at);

-- Production file lookup by session and type
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_production_files_session_type_ready 
ON production_files(session_id, file_type, print_ready);

-- Feedback analysis by rating and time
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_feedback_rating_created 
ON user_feedback(overall_rating, created_at DESC);

-- =====================================================
-- 2. SESSION TIMEOUT CONSTRAINTS
-- =====================================================

-- Add session timeout fields to existing table
ALTER TABLE design_sessions 
ADD COLUMN IF NOT EXISTS session_timeout_minutes INTEGER NOT NULL DEFAULT 60,
ADD COLUMN IF NOT EXISTS last_activity_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
ADD COLUMN IF NOT EXISTS expires_at TIMESTAMPTZ GENERATED ALWAYS AS (last_activity_at + INTERVAL '1 minute' * session_timeout_minutes) STORED;

-- Index for cleanup queries
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_design_sessions_expires_at 
ON design_sessions(expires_at) WHERE status = 'active';

-- Function to update last activity
CREATE OR REPLACE FUNCTION update_session_activity(session_uuid UUID)
RETURNS VOID AS $$
BEGIN
  UPDATE design_sessions 
  SET last_activity_at = NOW()
  WHERE id = session_uuid AND status = 'active';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to cleanup expired sessions
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS INTEGER AS $$
DECLARE
  expired_count INTEGER;
BEGIN
  UPDATE design_sessions 
  SET status = 'abandoned',
      updated_at = NOW()
  WHERE status = 'active' 
    AND expires_at < NOW();
  
  GET DIAGNOSTICS expired_count = ROW_COUNT;
  
  -- Log the cleanup
  INSERT INTO design_history (session_id, action_type, phase, step_number, action_description)
  SELECT id, 'session_abandoned', current_phase, 0, 'Auto-abandoned due to timeout'
  FROM design_sessions 
  WHERE status = 'abandoned' AND updated_at > NOW() - INTERVAL '1 minute';
  
  RETURN expired_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================================
-- 3. COST PREDICTION FUNCTION
-- =====================================================

CREATE OR REPLACE FUNCTION predict_session_cost(
  estimated_iterations INTEGER DEFAULT 4,
  target_quality generation_mode DEFAULT 'review'
)
RETURNS JSONB AS $$
DECLARE
  concept_cost NUMERIC(8,4);
  iteration_cost NUMERIC(8,4);
  production_cost NUMERIC(8,4);
  total_predicted NUMERIC(8,4);
  cost_breakdown JSONB;
BEGIN
  -- Get average costs by generation mode from historical data
  SELECT 
    COALESCE(AVG(CASE WHEN generation_mode = 'review' THEN cost END), 0.005) as avg_concept_cost,
    COALESCE(AVG(CASE WHEN generation_mode = target_quality THEN cost END), 0.005) as avg_iteration_cost,
    COALESCE(AVG(CASE WHEN generation_mode = 'production' THEN cost END), 0.19) as avg_production_cost
  INTO concept_cost, iteration_cost, production_cost
  FROM api_usage_log 
  WHERE success = true 
    AND created_at > NOW() - INTERVAL '30 days';
  
  -- Fallback to PRD estimates if no historical data
  IF concept_cost = 0 THEN concept_cost := 0.005; END IF;
  IF iteration_cost = 0 THEN iteration_cost := 0.005; END IF; 
  IF production_cost = 0 THEN production_cost := 0.19; END IF;
  
  -- Calculate prediction
  total_predicted := 
    (4 * concept_cost) +  -- 4 initial concepts
    (estimated_iterations * 4 * iteration_cost) +  -- 4 options per iteration
    (2 * production_cost);  -- Front + back cards
  
  -- Build breakdown
  cost_breakdown := jsonb_build_object(
    'concepts', jsonb_build_object(
      'count', 4,
      'unit_cost', concept_cost,
      'total_cost', 4 * concept_cost
    ),
    'iterations', jsonb_build_object(
      'rounds', estimated_iterations,
      'options_per_round', 4,
      'unit_cost', iteration_cost,
      'total_cost', estimated_iterations * 4 * iteration_cost
    ),
    'production', jsonb_build_object(
      'files', 2,
      'unit_cost', production_cost,
      'total_cost', 2 * production_cost
    ),
    'total_predicted', total_predicted,
    'target_quality', target_quality,
    'confidence', CASE 
      WHEN (SELECT COUNT(*) FROM api_usage_log WHERE created_at > NOW() - INTERVAL '30 days') > 100 THEN 'high'
      WHEN (SELECT COUNT(*) FROM api_usage_log WHERE created_at > NOW() - INTERVAL '30 days') > 20 THEN 'medium'
      ELSE 'low'
    END
  );
  
  RETURN cost_breakdown;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================================
-- 4. CONVERSION FUNNEL VIEW
-- =====================================================

CREATE OR REPLACE VIEW conversion_funnel AS
WITH session_stats AS (
  SELECT 
    ds.id,
    ds.status,
    ds.created_at::date as session_date,
    ds.current_phase,
    -- Concept stage
    CASE WHEN EXISTS(SELECT 1 FROM design_concepts WHERE session_id = ds.id) THEN 1 ELSE 0 END as has_concepts,
    -- Selection stages
    CASE WHEN EXISTS(SELECT 1 FROM user_selections WHERE session_id = ds.id AND phase = 'concept_selection') THEN 1 ELSE 0 END as selected_concept,
    CASE WHEN EXISTS(SELECT 1 FROM user_selections WHERE session_id = ds.id AND phase = 'layout_refinement') THEN 1 ELSE 0 END as selected_layout,
    CASE WHEN EXISTS(SELECT 1 FROM user_selections WHERE session_id = ds.id AND phase = 'typography_refinement') THEN 1 ELSE 0 END as selected_typography,
    CASE WHEN EXISTS(SELECT 1 FROM user_selections WHERE session_id = ds.id AND phase = 'color_refinement') THEN 1 ELSE 0 END as selected_color,
    -- Production stage
    CASE WHEN EXISTS(SELECT 1 FROM production_files WHERE session_id = ds.id AND print_ready = true) THEN 1 ELSE 0 END as has_production,
    -- Completion
    CASE WHEN ds.status = 'completed' THEN 1 ELSE 0 END as completed
  FROM design_sessions ds
),
daily_funnel AS (
  SELECT 
    session_date,
    COUNT(*) as sessions_started,
    SUM(has_concepts) as concepts_generated,
    SUM(selected_concept) as concept_selections,
    SUM(selected_layout) as layout_selections,
    SUM(selected_typography) as typography_selections,
    SUM(selected_color) as color_selections,
    SUM(has_production) as production_files,
    SUM(completed) as sessions_completed
  FROM session_stats
  GROUP BY session_date
)
SELECT 
  session_date,
  sessions_started,
  concepts_generated,
  concept_selections,
  layout_selections,
  typography_selections,
  color_selections,
  production_files,
  sessions_completed,
  -- Conversion rates
  ROUND(100.0 * concepts_generated / NULLIF(sessions_started, 0), 2) as concept_generation_rate,
  ROUND(100.0 * concept_selections / NULLIF(concepts_generated, 0), 2) as concept_selection_rate,
  ROUND(100.0 * layout_selections / NULLIF(concept_selections, 0), 2) as layout_selection_rate,
  ROUND(100.0 * typography_selections / NULLIF(layout_selections, 0), 2) as typography_selection_rate,
  ROUND(100.0 * color_selections / NULLIF(typography_selections, 0), 2) as color_selection_rate,
  ROUND(100.0 * production_files / NULLIF(color_selections, 0), 2) as production_rate,
  ROUND(100.0 * sessions_completed / NULLIF(sessions_started, 0), 2) as overall_completion_rate
FROM daily_funnel
ORDER BY session_date DESC;

-- =====================================================
-- 5. PERFORMANCE MONITORING
-- =====================================================

-- Performance log table
CREATE TABLE IF NOT EXISTS performance_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  query_type TEXT NOT NULL,
  duration_ms INTEGER NOT NULL,
  table_name TEXT,
  operation TEXT, -- INSERT, UPDATE, SELECT, DELETE
  row_count INTEGER,
  session_id UUID REFERENCES design_sessions(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for performance analysis
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_performance_log_query_duration 
ON performance_log(query_type, duration_ms DESC, created_at);

-- Function to log slow queries
CREATE OR REPLACE FUNCTION log_slow_queries() 
RETURNS TRIGGER AS $$
DECLARE
  duration_ms INTEGER;
BEGIN
  -- Calculate duration since statement start
  duration_ms := EXTRACT(EPOCH FROM (clock_timestamp() - statement_timestamp())) * 1000;
  
  -- Log queries taking >1 second
  IF duration_ms > 1000 THEN
    INSERT INTO performance_log (query_type, duration_ms, table_name, operation, created_at)
    VALUES (TG_OP, duration_ms, TG_TABLE_NAME, TG_OP, NOW());
  END IF;
  
  RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Add performance monitoring triggers to key tables
DROP TRIGGER IF EXISTS perf_monitor_design_sessions ON design_sessions;
CREATE TRIGGER perf_monitor_design_sessions
  AFTER INSERT OR UPDATE OR DELETE ON design_sessions
  FOR EACH ROW EXECUTE FUNCTION log_slow_queries();

DROP TRIGGER IF EXISTS perf_monitor_design_iterations ON design_iterations;
CREATE TRIGGER perf_monitor_design_iterations
  AFTER INSERT OR UPDATE OR DELETE ON design_iterations
  FOR EACH ROW EXECUTE FUNCTION log_slow_queries();

-- Performance analytics view
CREATE OR REPLACE VIEW performance_analytics AS
SELECT 
  query_type,
  table_name,
  operation,
  COUNT(*) as slow_query_count,
  AVG(duration_ms) as avg_duration_ms,
  MAX(duration_ms) as max_duration_ms,
  MIN(duration_ms) as min_duration_ms,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY duration_ms) as p95_duration_ms
FROM performance_log
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY query_type, table_name, operation
ORDER BY avg_duration_ms DESC;

-- =====================================================
-- 6. ENHANCED SESSION PROGRESS TRACKING
-- =====================================================

-- Enhanced session progress with timing analysis
CREATE OR REPLACE FUNCTION get_enhanced_session_progress(session_uuid UUID)
RETURNS JSONB AS $$
DECLARE
  result JSONB;
  session_info RECORD;
  phase_timings JSONB;
  cost_info JSONB;
BEGIN
  -- Get session info
  SELECT 
    current_phase,
    status,
    created_at,
    last_activity_at,
    expires_at,
    calculate_session_cost(id) as current_cost
  INTO session_info
  FROM design_sessions 
  WHERE id = session_uuid;
  
  -- Get phase timings
  WITH phase_times AS (
    SELECT 
      phase,
      MIN(created_at) as started_at,
      MAX(created_at) as completed_at,
      COUNT(*) as actions_count
    FROM design_history 
    WHERE session_id = session_uuid
    GROUP BY phase
  )
  SELECT jsonb_object_agg(
    phase::text, 
    jsonb_build_object(
      'started_at', started_at,
      'completed_at', completed_at,
      'duration_seconds', EXTRACT(EPOCH FROM (completed_at - started_at)),
      'actions_count', actions_count
    )
  ) INTO phase_timings
  FROM phase_times;
  
  -- Get cost prediction
  SELECT predict_session_cost() INTO cost_info;
  
  -- Build comprehensive progress object
  result := jsonb_build_object(
    'current_phase', session_info.current_phase,
    'status', session_info.status,
    'session_age_minutes', EXTRACT(EPOCH FROM (NOW() - session_info.created_at)) / 60,
    'time_until_expiry_minutes', EXTRACT(EPOCH FROM (session_info.expires_at - NOW())) / 60,
    'current_cost', session_info.current_cost,
    'cost_prediction', cost_info,
    'phase_timings', COALESCE(phase_timings, '{}'::jsonb),
    'progress_percentage', CASE session_info.current_phase
      WHEN 'concept_selection' THEN 20
      WHEN 'layout_refinement' THEN 40  
      WHEN 'typography_refinement' THEN 60
      WHEN 'color_refinement' THEN 80
      WHEN 'final_production' THEN 100
      ELSE 0
    END
  );
  
  RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================================
-- 7. ANALYTICS HELPER FUNCTIONS
-- =====================================================

-- Get conversion metrics for a date range
CREATE OR REPLACE FUNCTION get_conversion_metrics(
  start_date DATE DEFAULT CURRENT_DATE - INTERVAL '7 days',
  end_date DATE DEFAULT CURRENT_DATE
)
RETURNS JSONB AS $$
DECLARE
  metrics JSONB;
BEGIN
  WITH funnel_data AS (
    SELECT * FROM conversion_funnel 
    WHERE session_date BETWEEN start_date AND end_date
  ),
  aggregated AS (
    SELECT 
      SUM(sessions_started) as total_sessions,
      SUM(sessions_completed) as total_completed,
      AVG(overall_completion_rate) as avg_completion_rate,
      AVG(concept_selection_rate) as avg_concept_selection_rate,
      AVG(production_rate) as avg_production_rate
    FROM funnel_data
  )
  SELECT jsonb_build_object(
    'date_range', jsonb_build_object(
      'start_date', start_date,
      'end_date', end_date
    ),
    'totals', jsonb_build_object(
      'sessions_started', total_sessions,
      'sessions_completed', total_completed,
      'completion_rate', ROUND(100.0 * total_completed / NULLIF(total_sessions, 0), 2)
    ),
    'averages', jsonb_build_object(
      'avg_completion_rate', ROUND(avg_completion_rate, 2),
      'avg_concept_selection_rate', ROUND(avg_concept_selection_rate, 2),
      'avg_production_rate', ROUND(avg_production_rate, 2)
    )
  ) INTO metrics
  FROM aggregated;
  
  RETURN metrics;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Get cost efficiency metrics
CREATE OR REPLACE FUNCTION get_cost_efficiency_metrics()
RETURNS JSONB AS $$
DECLARE
  metrics JSONB;
BEGIN
  WITH cost_data AS (
    SELECT 
      ds.id,
      ds.status,
      calculate_session_cost(ds.id) as session_cost,
      COUNT(pf.id) as production_files_count
    FROM design_sessions ds
    LEFT JOIN production_files pf ON ds.id = pf.session_id
    WHERE ds.created_at > NOW() - INTERVAL '30 days'
    GROUP BY ds.id, ds.status
  )
  SELECT jsonb_build_object(
    'avg_cost_per_session', ROUND(AVG(session_cost), 4),
    'avg_cost_per_completed_session', ROUND(AVG(session_cost) FILTER (WHERE status = 'completed'), 4),
    'avg_cost_per_production_file', ROUND(AVG(session_cost / NULLIF(production_files_count, 0)) FILTER (WHERE production_files_count > 0), 4),
    'total_cost_last_30_days', ROUND(SUM(session_cost), 2),
    'completed_sessions_last_30_days', COUNT(*) FILTER (WHERE status = 'completed')
  ) INTO metrics
  FROM cost_data;
  
  RETURN metrics;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================================
-- 8. AUTOMATED MAINTENANCE
-- =====================================================

-- Create a maintenance log
CREATE TABLE IF NOT EXISTS maintenance_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_name TEXT NOT NULL,
  rows_affected INTEGER,
  duration_ms INTEGER,
  success BOOLEAN NOT NULL DEFAULT TRUE,
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Automated cleanup function (run daily via cron/scheduler)
CREATE OR REPLACE FUNCTION daily_maintenance()
RETURNS JSONB AS $$
DECLARE
  start_time TIMESTAMPTZ;
  end_time TIMESTAMPTZ;
  expired_sessions INTEGER;
  old_logs_deleted INTEGER;
  result JSONB;
BEGIN
  start_time := clock_timestamp();
  
  -- Cleanup expired sessions
  SELECT cleanup_expired_sessions() INTO expired_sessions;
  
  -- Cleanup old performance logs (keep 30 days)
  DELETE FROM performance_log 
  WHERE created_at < NOW() - INTERVAL '30 days';
  GET DIAGNOSTICS old_logs_deleted = ROW_COUNT;
  
  end_time := clock_timestamp();
  
  -- Log maintenance results
  result := jsonb_build_object(
    'expired_sessions_cleaned', expired_sessions,
    'old_performance_logs_deleted', old_logs_deleted,
    'duration_ms', EXTRACT(EPOCH FROM (end_time - start_time)) * 1000,
    'completed_at', end_time
  );
  
  INSERT INTO maintenance_log (task_name, rows_affected, duration_ms, success)
  VALUES ('daily_maintenance', expired_sessions + old_logs_deleted, 
          EXTRACT(EPOCH FROM (end_time - start_time)) * 1000, TRUE);
  
  RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================================
-- 9. ENHANCED VIEWS WITH BETTER PERFORMANCE
-- =====================================================

-- Fast session summary (materialized view candidate)
CREATE OR REPLACE VIEW session_summary_fast AS
SELECT 
  ds.id,
  ds.user_id,
  ds.session_name,
  ds.status,
  ds.current_phase,
  ds.created_at,
  ds.last_activity_at,
  ds.total_cost,
  -- Pre-calculated counts to avoid joins
  (SELECT COUNT(*) FROM design_concepts WHERE session_id = ds.id) as concepts_count,
  (SELECT COUNT(*) FROM design_iterations WHERE session_id = ds.id) as iterations_count,
  (SELECT COUNT(*) FROM user_selections WHERE session_id = ds.id) as selections_count,
  (SELECT COUNT(*) FROM production_files WHERE session_id = ds.id) as production_files_count,
  -- Quick progress calculation
  CASE ds.current_phase
    WHEN 'concept_selection' THEN 20
    WHEN 'layout_refinement' THEN 40
    WHEN 'typography_refinement' THEN 60
    WHEN 'color_refinement' THEN 80
    WHEN 'final_production' THEN 100
    ELSE 0
  END as progress_percentage
FROM design_sessions ds;

-- =====================================================
-- 10. GRANTS AND FINAL SETUP
-- =====================================================

-- Grant access to new functions
GRANT EXECUTE ON FUNCTION update_session_activity(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION predict_session_cost(INTEGER, generation_mode) TO authenticated;
GRANT EXECUTE ON FUNCTION get_enhanced_session_progress(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION get_conversion_metrics(DATE, DATE) TO service_role;
GRANT EXECUTE ON FUNCTION get_cost_efficiency_metrics() TO service_role;
GRANT EXECUTE ON FUNCTION daily_maintenance() TO service_role;

-- Grant access to new views
GRANT SELECT ON conversion_funnel TO authenticated, service_role;
GRANT SELECT ON performance_analytics TO service_role;
GRANT SELECT ON session_summary_fast TO authenticated;

-- Update schema version
UPDATE schema_migrations 
SET applied_at = NOW() 
WHERE version = 2;

-- =====================================================
-- QUICK VERIFICATION QUERIES
-- =====================================================

/*
-- Test cost prediction
SELECT predict_session_cost(4, 'review'::generation_mode);

-- Test session progress
SELECT get_enhanced_session_progress('00000000-0000-0000-0000-000000000000'::uuid);

-- View conversion funnel
SELECT * FROM conversion_funnel ORDER BY session_date DESC LIMIT 7;

-- Check performance
SELECT * FROM performance_analytics;

-- Test maintenance
SELECT daily_maintenance();
*/

-- =====================================================
-- END OF ENHANCEMENTS
-- =====================================================