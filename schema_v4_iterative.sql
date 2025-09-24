-- =====================================================
-- Business Card Generator v4.0 - Iterative Design System
-- Supabase/Postgres Schema
-- =====================================================

-- Enable necessary extensions
create extension if not exists "uuid-ossp";

-- =====================================================
-- ENUMS
-- =====================================================

-- Design concepts from PRD
create type concept_type as enum (
  'clinical_precision',     -- Medical authority focus
  'athletic_edge',         -- Performance and strength  
  'luxury_wellness',       -- Premium spa aesthetic
  'minimalist_pro'         -- Clean, simple elegance
);

-- Refinement categories from PRD
create type refinement_type as enum (
  'layout',               -- positioning, alignment, spacing, proportions
  'typography',           -- font_choice, weights, sizing, letter_spacing
  'colors',              -- accent_placement, color_intensity, gradients, contrast
  'elements',            -- logo_size, qr_placement, borders, textures
  'style'                -- minimalism, boldness, elegance, energy
);

-- Generation modes with cost tracking
create type generation_mode as enum (
  'draft',               -- Fast Gemini generation (~$0.001)
  'review',              -- Standard quality (~$0.005)
  'production'           -- High-quality GPT Image 1 (~$0.19)
);

-- AI models used
create type ai_model as enum (
  'gemini_nano',
  'gemini_flash',
  'gemini_2_5_flash_image',
  'gpt_image_1'
);

-- Session status
create type session_status as enum (
  'active',              -- Currently in progress
  'completed',           -- User finished and approved final design
  'abandoned',           -- User left without completing
  'error'                -- System error occurred
);

-- Iteration phase tracking
create type iteration_phase as enum (
  'concept_selection',    -- Initial 4 concept variations
  'layout_refinement',   -- 4 layout options
  'typography_refinement', -- 4 typography variations
  'color_refinement',    -- 4 color/accent variations
  'element_refinement',  -- Additional element adjustments
  'final_production'     -- High-res production generation
);

-- =====================================================
-- CORE TABLES
-- =====================================================

-- Design Sessions - Track each user's design journey
create table design_sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  session_name text not null default 'Untitled Session',
  status session_status not null default 'active',
  current_phase iteration_phase not null default 'concept_selection',
  total_cost numeric(10,4) not null default 0.00,
  estimated_iterations integer not null default 4,
  actual_iterations integer not null default 0,
  final_selection_path text, -- e.g., "B-3-b-ii" from PRD example
  
  -- Timestamps
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  completed_at timestamptz,
  
  -- Metadata
  user_agent text,
  ip_address inet,
  referrer text
);

-- Design Concepts - The 4 initial variations generated
create table design_concepts (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references design_sessions(id) on delete cascade,
  concept_type concept_type not null,
  concept_label varchar(1) not null, -- A, B, C, D
  
  -- Generation details
  ai_model ai_model not null,
  generation_mode generation_mode not null,
  prompt_used text not null,
  generation_cost numeric(8,4) not null,
  generation_time_ms integer not null,
  
  -- Image data
  image_url text not null,
  image_size_bytes integer not null,
  image_width integer not null,
  image_height integer not null,
  image_format varchar(10) not null default 'png',
  
  -- Timestamps
  created_at timestamptz not null default now(),
  
  -- Constraints
  constraint unique_concept_per_session unique (session_id, concept_label),
  constraint valid_concept_label check (concept_label in ('A', 'B', 'C', 'D'))
);

-- User Selections - Track user choices at each phase
create table user_selections (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references design_sessions(id) on delete cascade,
  phase iteration_phase not null,
  phase_order integer not null, -- Multiple refinements of same type
  
  -- Selection details
  selected_option varchar(10) not null, -- A, B, C, D or 1, 2, 3, 4 or a, b, c, d or i, ii, iii, iv
  selected_concept_id uuid references design_concepts(id) on delete set null,
  selected_iteration_id uuid references design_iterations(id) on delete set null,
  
  -- User feedback
  user_feedback text,
  satisfaction_rating integer check (satisfaction_rating between 1 and 5),
  
  -- Timing
  time_to_select_ms integer not null,
  created_at timestamptz not null default now(),
  
  -- Constraints
  constraint valid_rating check (satisfaction_rating is null or satisfaction_rating between 1 and 5)
);

-- Design Iterations - All refinement variations generated
create table design_iterations (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references design_sessions(id) on delete cascade,
  parent_concept_id uuid references design_concepts(id) on delete cascade,
  parent_iteration_id uuid references design_iterations(id) on delete cascade,
  
  -- Iteration details
  phase iteration_phase not null,
  refinement_type refinement_type not null,
  iteration_label varchar(10) not null, -- 1,2,3,4 then a,b,c,d then i,ii,iii,iv
  iteration_order integer not null, -- Order within session
  
  -- Generation details
  ai_model ai_model not null,
  generation_mode generation_mode not null,
  prompt_used text not null,
  prompt_delta text, -- What changed from parent
  generation_cost numeric(8,4) not null,
  generation_time_ms integer not null,
  
  -- Image data
  image_url text not null,
  image_size_bytes integer not null,
  image_width integer not null,
  image_height integer not null,
  image_format varchar(10) not null default 'png',
  
  -- Metadata
  refinement_description text, -- Human readable description of the change
  technical_parameters jsonb, -- Store specific adjustments made
  
  -- Timestamps
  created_at timestamptz not null default now(),
  
  -- Constraints
  constraint parent_concept_or_iteration check (
    (parent_concept_id is not null and parent_iteration_id is null) or
    (parent_concept_id is null and parent_iteration_id is not null)
  )
);

-- Design History - Complete audit trail of the design journey
create table design_history (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references design_sessions(id) on delete cascade,
  
  -- History entry details
  action_type varchar(50) not null, -- 'concept_generated', 'iteration_created', 'user_selection', 'refinement_requested'
  phase iteration_phase not null,
  step_number integer not null,
  
  -- Related entities
  concept_id uuid references design_concepts(id) on delete set null,
  iteration_id uuid references design_iterations(id) on delete set null,
  selection_id uuid references user_selections(id) on delete set null,
  
  -- Action details
  action_description text not null,
  metadata jsonb, -- Store flexible metadata about the action
  
  -- Timing
  created_at timestamptz not null default now(),
  
  -- Constraints
  constraint valid_action_type check (action_type in (
    'session_started',
    'concept_generated', 
    'concept_selected',
    'iteration_created',
    'iteration_selected', 
    'refinement_requested',
    'production_generated',
    'session_completed',
    'session_abandoned',
    'error_occurred'
  ))
);

-- Production Files - Final high-resolution outputs
create table production_files (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references design_sessions(id) on delete cascade,
  final_iteration_id uuid references design_iterations(id) on delete set null,
  
  -- File details
  file_type varchar(20) not null, -- 'front_card', 'back_card', 'design_report'
  file_name text not null,
  file_url text not null,
  file_size_bytes integer not null,
  file_format varchar(10) not null,
  
  -- Production specs (for print-ready files)
  dpi integer, -- 300+ for professional printing
  width_inches numeric(4,2), -- 3.5" for business cards
  height_inches numeric(4,2), -- 2.0" for business cards
  color_profile varchar(20), -- RGB, CMYK
  
  -- Generation details
  ai_model ai_model not null,
  generation_cost numeric(8,4) not null,
  generation_time_ms integer not null,
  prompt_used text not null,
  
  -- Quality metrics
  quality_score integer check (quality_score between 1 and 10),
  print_ready boolean not null default false,
  
  -- Timestamps
  created_at timestamptz not null default now(),
  
  -- Constraints
  constraint valid_file_type check (file_type in ('front_card', 'back_card', 'design_report')),
  constraint valid_dimensions check (
    (file_type in ('front_card', 'back_card') and width_inches = 3.5 and height_inches = 2.0) or
    file_type not in ('front_card', 'back_card')
  )
);

-- API Usage Tracking - Monitor costs and performance
create table api_usage_log (
  id uuid primary key default gen_random_uuid(),
  session_id uuid references design_sessions(id) on delete set null,
  
  -- API call details
  ai_model ai_model not null,
  generation_mode generation_mode not null,
  operation_type varchar(30) not null, -- 'concept_generation', 'iteration_refinement', 'production_generation'
  
  -- Cost and performance
  cost numeric(8,4) not null,
  duration_ms integer not null,
  tokens_used integer,
  
  -- Request/response
  request_payload jsonb,
  response_metadata jsonb,
  
  -- Status
  success boolean not null default true,
  error_message text,
  
  -- Timestamps
  created_at timestamptz not null default now(),
  
  -- Constraints
  constraint valid_operation_type check (operation_type in (
    'concept_generation',
    'layout_refinement',
    'typography_refinement', 
    'color_refinement',
    'element_refinement',
    'production_generation'
  ))
);

-- User Feedback - Collect user satisfaction and suggestions
create table user_feedback (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references design_sessions(id) on delete cascade,
  user_id uuid references auth.users(id) on delete set null,
  
  -- Feedback details
  feedback_type varchar(30) not null, -- 'iteration_feedback', 'final_feedback', 'bug_report'
  overall_rating integer not null check (overall_rating between 1 and 5),
  ease_of_use_rating integer check (ease_of_use_rating between 1 and 5),
  design_quality_rating integer check (design_quality_rating between 1 and 5),
  speed_rating integer check (speed_rating between 1 and 5),
  
  -- Text feedback
  feedback_text text,
  suggestions text,
  
  -- Context
  phase_completed iteration_phase,
  iterations_used integer,
  total_time_minutes integer,
  
  -- Timestamps
  created_at timestamptz not null default now(),
  
  -- Constraints
  constraint valid_feedback_type check (feedback_type in (
    'iteration_feedback',
    'final_feedback', 
    'bug_report',
    'feature_request'
  ))
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Session lookup indexes
create index idx_design_sessions_user_id on design_sessions(user_id);
create index idx_design_sessions_status on design_sessions(status);
create index idx_design_sessions_created_at on design_sessions(created_at desc);
create index idx_design_sessions_current_phase on design_sessions(current_phase);

-- Concept lookup indexes  
create index idx_design_concepts_session_id on design_concepts(session_id);
create index idx_design_concepts_concept_type on design_concepts(concept_type);
create index idx_design_concepts_created_at on design_concepts(created_at desc);

-- Iteration lookup indexes
create index idx_design_iterations_session_id on design_iterations(session_id);
create index idx_design_iterations_parent_concept_id on design_iterations(parent_concept_id);
create index idx_design_iterations_parent_iteration_id on design_iterations(parent_iteration_id);
create index idx_design_iterations_phase on design_iterations(phase);
create index idx_design_iterations_refinement_type on design_iterations(refinement_type);

-- Selection tracking indexes
create index idx_user_selections_session_id on user_selections(session_id);
create index idx_user_selections_phase on user_selections(phase);
create index idx_user_selections_created_at on user_selections(created_at desc);

-- History tracking indexes
create index idx_design_history_session_id on design_history(session_id);
create index idx_design_history_action_type on design_history(action_type);
create index idx_design_history_created_at on design_history(created_at desc);

-- Production file indexes
create index idx_production_files_session_id on production_files(session_id);
create index idx_production_files_file_type on production_files(file_type);
create index idx_production_files_print_ready on production_files(print_ready);

-- API usage indexes for cost tracking
create index idx_api_usage_log_session_id on api_usage_log(session_id);
create index idx_api_usage_log_ai_model on api_usage_log(ai_model);
create index idx_api_usage_log_created_at on api_usage_log(created_at desc);
create index idx_api_usage_log_cost on api_usage_log(cost desc);

-- Feedback indexes
create index idx_user_feedback_session_id on user_feedback(session_id);
create index idx_user_feedback_overall_rating on user_feedback(overall_rating);
create index idx_user_feedback_created_at on user_feedback(created_at desc);

-- =====================================================
-- FUNCTIONS & TRIGGERS
-- =====================================================

-- Function to update updated_at timestamp
create or replace function update_updated_at_column()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

-- Trigger for design_sessions updated_at
create trigger update_design_sessions_updated_at
  before update on design_sessions
  for each row execute function update_updated_at_column();

-- Function to calculate session cost
create or replace function calculate_session_cost(session_uuid uuid)
returns numeric as $$
declare
  total_cost numeric(10,4) := 0;
begin
  -- Sum costs from concepts
  select coalesce(sum(generation_cost), 0) into total_cost
  from design_concepts 
  where session_id = session_uuid;
  
  -- Add costs from iterations
  select total_cost + coalesce(sum(generation_cost), 0) into total_cost
  from design_iterations 
  where session_id = session_uuid;
  
  -- Add costs from production files
  select total_cost + coalesce(sum(generation_cost), 0) into total_cost
  from production_files 
  where session_id = session_uuid;
  
  return total_cost;
end;
$$ language plpgsql;

-- Function to get session progress
create or replace function get_session_progress(session_uuid uuid)
returns jsonb as $$
declare
  result jsonb;
  concept_count integer;
  iteration_count integer;
  selection_count integer;
  current_phase_text text;
begin
  -- Get basic session info
  select 
    s.current_phase::text,
    s.actual_iterations,
    s.status::text
  into current_phase_text, iteration_count, result
  from design_sessions s 
  where s.id = session_uuid;
  
  -- Count concepts generated
  select count(*) into concept_count
  from design_concepts
  where session_id = session_uuid;
  
  -- Count total iterations
  select count(*) into iteration_count  
  from design_iterations
  where session_id = session_uuid;
  
  -- Count user selections made
  select count(*) into selection_count
  from user_selections  
  where session_id = session_uuid;
  
  -- Build progress object
  result := jsonb_build_object(
    'current_phase', current_phase_text,
    'concepts_generated', concept_count,
    'iterations_created', iteration_count, 
    'selections_made', selection_count,
    'progress_percentage', case 
      when current_phase_text = 'concept_selection' then 25
      when current_phase_text = 'layout_refinement' then 45  
      when current_phase_text = 'typography_refinement' then 65
      when current_phase_text = 'color_refinement' then 85
      when current_phase_text = 'final_production' then 100
      else 0
    end
  );
  
  return result;
end;
$$ language plpgsql;

-- =====================================================
-- RLS POLICIES (Row Level Security)
-- =====================================================

-- Enable RLS on all tables
alter table design_sessions enable row level security;
alter table design_concepts enable row level security;  
alter table design_iterations enable row level security;
alter table user_selections enable row level security;
alter table design_history enable row level security;
alter table production_files enable row level security;
alter table api_usage_log enable row level security;
alter table user_feedback enable row level security;

-- Design Sessions - Users can only access their own sessions
create policy "Users can view own design sessions" on design_sessions
  for select using (auth.uid() = user_id);

create policy "Users can create own design sessions" on design_sessions  
  for insert with check (auth.uid() = user_id);

create policy "Users can update own design sessions" on design_sessions
  for update using (auth.uid() = user_id);

-- Design Concepts - Access via session ownership
create policy "Users can view concepts from own sessions" on design_concepts
  for select using (
    session_id in (
      select id from design_sessions where user_id = auth.uid()
    )
  );

create policy "Users can create concepts for own sessions" on design_concepts
  for insert with check (
    session_id in (
      select id from design_sessions where user_id = auth.uid()  
    )
  );

-- Design Iterations - Access via session ownership
create policy "Users can view iterations from own sessions" on design_iterations
  for select using (
    session_id in (
      select id from design_sessions where user_id = auth.uid()
    )
  );

create policy "Users can create iterations for own sessions" on design_iterations
  for insert with check (
    session_id in (
      select id from design_sessions where user_id = auth.uid()
    )
  );

-- User Selections - Access via session ownership
create policy "Users can view own selections" on user_selections
  for select using (
    session_id in (
      select id from design_sessions where user_id = auth.uid()
    )
  );

create policy "Users can create own selections" on user_selections
  for insert with check (
    session_id in (
      select id from design_sessions where user_id = auth.uid()
    )
  );

-- Design History - Read-only access via session ownership
create policy "Users can view own design history" on design_history
  for select using (
    session_id in (
      select id from design_sessions where user_id = auth.uid()
    )
  );

-- Production Files - Access via session ownership
create policy "Users can view own production files" on production_files
  for select using (
    session_id in (
      select id from design_sessions where user_id = auth.uid()
    )
  );

-- API Usage Log - Read-only for users, full access for service role
create policy "Users can view api usage for own sessions" on api_usage_log
  for select using (
    session_id in (
      select id from design_sessions where user_id = auth.uid()
    )
  );

-- User Feedback - Users can manage their own feedback
create policy "Users can view own feedback" on user_feedback
  for select using (user_id = auth.uid());

create policy "Users can create own feedback" on user_feedback
  for insert with check (user_id = auth.uid());

create policy "Users can update own feedback" on user_feedback  
  for update using (user_id = auth.uid());

-- =====================================================
-- SAMPLE DATA FOR TESTING
-- =====================================================

-- Insert sample data (commented out for production)
/*
-- Sample design session
insert into design_sessions (id, user_id, session_name, status, current_phase)
values (
  '550e8400-e29b-41d4-a716-446655440000',
  auth.uid(),
  'Alex Shafiro PT - Athletic Edge Design',
  'active',
  'concept_selection'
);

-- Sample concepts
insert into design_concepts (session_id, concept_type, concept_label, ai_model, generation_mode, prompt_used, generation_cost, generation_time_ms, image_url, image_size_bytes, image_width, image_height)
values 
  ('550e8400-e29b-41d4-a716-446655440000', 'clinical_precision', 'A', 'gemini_flash', 'review', 'Clinical precision business card...', 0.005, 3200, 'https://example.com/concept-a.png', 245678, 1024, 1024),
  ('550e8400-e29b-41d4-a716-446655440000', 'athletic_edge', 'B', 'gemini_flash', 'review', 'Athletic edge business card...', 0.005, 3100, 'https://example.com/concept-b.png', 251234, 1024, 1024),
  ('550e8400-e29b-41d4-a716-446655440000', 'luxury_wellness', 'C', 'gemini_flash', 'review', 'Luxury wellness business card...', 0.005, 3300, 'https://example.com/concept-c.png', 248901, 1024, 1024),
  ('550e8400-e29b-41d4-a716-446655440000', 'minimalist_pro', 'D', 'gemini_flash', 'review', 'Minimalist professional business card...', 0.005, 2900, 'https://example.com/concept-d.png', 239456, 1024, 1024);
*/

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- Session overview with costs and progress
create view session_overview as
select 
  ds.id,
  ds.session_name,
  ds.status,
  ds.current_phase,
  ds.created_at,
  ds.updated_at,
  calculate_session_cost(ds.id) as total_cost,
  get_session_progress(ds.id) as progress,
  count(dc.id) as concepts_generated,
  count(di.id) as iterations_created,
  count(us.id) as selections_made,
  count(pf.id) as production_files_created
from design_sessions ds
left join design_concepts dc on ds.id = dc.session_id
left join design_iterations di on ds.id = di.session_id  
left join user_selections us on ds.id = us.session_id
left join production_files pf on ds.id = pf.session_id
group by ds.id, ds.session_name, ds.status, ds.current_phase, ds.created_at, ds.updated_at;

-- Cost analysis view
create view cost_analysis as
select 
  ai_model,
  generation_mode,
  count(*) as usage_count,
  avg(cost) as avg_cost,
  sum(cost) as total_cost,
  avg(duration_ms) as avg_duration_ms
from api_usage_log
where success = true
group by ai_model, generation_mode
order by total_cost desc;

-- User satisfaction view  
create view user_satisfaction as
select
  feedback_type,
  avg(overall_rating) as avg_overall_rating,
  avg(ease_of_use_rating) as avg_ease_rating,
  avg(design_quality_rating) as avg_quality_rating,
  avg(speed_rating) as avg_speed_rating,
  count(*) as feedback_count
from user_feedback
group by feedback_type
order by avg_overall_rating desc;

-- =====================================================
-- COMMENTS FOR DOCUMENTATION
-- =====================================================

comment on table design_sessions is 'Tracks each user design journey from concept to production';
comment on table design_concepts is 'Initial 4 concept variations (Clinical, Athletic, Luxury, Minimalist)';  
comment on table design_iterations is 'All refinement variations generated during iterative process';
comment on table user_selections is 'User choices at each phase (A/B/C/D, 1/2/3/4, a/b/c/d, i/ii/iii/iv)';
comment on table design_history is 'Complete audit trail of design journey for reproducibility';
comment on table production_files is 'Final high-resolution print-ready files';
comment on table api_usage_log is 'API call tracking for cost monitoring and performance analysis';
comment on table user_feedback is 'User satisfaction and feedback collection';

comment on type concept_type is 'Four design concepts: Clinical Precision, Athletic Edge, Luxury Wellness, Minimalist Pro';
comment on type refinement_type is 'Categories of refinement: layout, typography, colors, elements, style';
comment on type generation_mode is 'Quality levels: draft ($0.001), review ($0.005), production ($0.19)';
comment on type iteration_phase is 'Phases of iterative design process from concept to production';

-- =====================================================
-- GRANTS (if needed for service roles)
-- =====================================================

-- Grant necessary permissions to authenticated users
grant usage on schema public to authenticated;
grant all on all tables in schema public to authenticated;
grant all on all sequences in schema public to authenticated;

-- Grant permissions to service role for background tasks
grant all on all tables in schema public to service_role;
grant all on all sequences in schema public to service_role;

-- =====================================================
-- END OF SCHEMA
-- =====================================================