#!/usr/bin/env python3
"""
Metrics Collection and Monitoring System

Comprehensive monitoring, metrics collection, and alerting for the
Business Card Generator API service.
"""

import time
import psutil
import threading
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, field

import structlog
from prometheus_client import Counter, Histogram, Gauge, Info, CollectorRegistry

logger = structlog.get_logger(__name__)

@dataclass
class MetricsSummary:
    """Summary of key metrics"""
    requests_total: int = 0
    requests_successful: int = 0
    requests_failed: int = 0
    avg_response_time: float = 0.0
    generation_requests: int = 0
    generation_successful: int = 0
    cache_hit_rate: float = 0.0
    total_cost_estimate: float = 0.0
    uptime_seconds: float = 0.0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0

class MetricsCollector:
    """Comprehensive metrics collection system"""
    
    def __init__(self, collection_interval: int = 60):
        """
        Initialize metrics collector
        
        Args:
            collection_interval: Interval in seconds for metric collection
        """
        self.collection_interval = collection_interval
        self.start_time = time.time()
        
        # Internal metrics storage
        self.metrics = defaultdict(int)
        self.timeseries_metrics = defaultdict(lambda: deque(maxlen=1440))  # 24 hours at 1min intervals
        self.gauges = defaultdict(float)
        self.response_times = deque(maxlen=1000)
        
        # Prometheus metrics
        self.registry = CollectorRegistry()
        self._setup_prometheus_metrics()
        
        # Background collection thread
        self.collection_thread = None
        self.should_collect = False
        
        logger.info("Metrics collector initialized", collection_interval=collection_interval)
    
    def _setup_prometheus_metrics(self):
        """Setup Prometheus metrics"""
        self.prom_metrics = {
            'requests_total': Counter(
                'bcg_requests_total', 
                'Total requests processed',
                ['method', 'endpoint', 'status'],
                registry=self.registry
            ),
            'request_duration': Histogram(
                'bcg_request_duration_seconds',
                'Request duration in seconds',
                ['method', 'endpoint'],
                registry=self.registry
            ),
            'generation_requests': Counter(
                'bcg_generation_requests_total',
                'Total generation requests',
                ['model', 'concept', 'quality'],
                registry=self.registry
            ),
            'generation_duration': Histogram(
                'bcg_generation_duration_seconds',
                'Generation duration in seconds',
                ['model', 'concept'],
                registry=self.registry
            ),
            'cache_operations': Counter(
                'bcg_cache_operations_total',
                'Cache operations',
                ['operation', 'result'],
                registry=self.registry
            ),
            'active_jobs': Gauge(
                'bcg_active_jobs',
                'Number of active generation jobs',
                registry=self.registry
            ),
            'memory_usage': Gauge(
                'bcg_memory_usage_bytes',
                'Memory usage in bytes',
                registry=self.registry
            ),
            'cpu_usage': Gauge(
                'bcg_cpu_usage_percent',
                'CPU usage percentage',
                registry=self.registry
            ),
            'uptime': Gauge(
                'bcg_uptime_seconds',
                'Service uptime in seconds',
                registry=self.registry
            ),
            'system_info': Info(
                'bcg_system_info',
                'System information',
                registry=self.registry
            )
        }
        
        # Set system info
        self.prom_metrics['system_info'].info({
            'version': '4.0.0',
            'python_version': f"{psutil.python_version()}",
            'platform': psutil.platform(),
        })
    
    def start_collection(self):
        """Start background metrics collection"""
        if self.collection_thread and self.collection_thread.is_alive():
            return
        
        self.should_collect = True
        self.collection_thread = threading.Thread(target=self._collect_system_metrics)
        self.collection_thread.daemon = True
        self.collection_thread.start()
        
        logger.info("Background metrics collection started")
    
    def stop_collection(self):
        """Stop background metrics collection"""
        self.should_collect = False
        if self.collection_thread:
            self.collection_thread.join(timeout=5)
        
        logger.info("Background metrics collection stopped")
    
    def _collect_system_metrics(self):
        """Background thread for system metrics collection"""
        while self.should_collect:
            try:
                current_time = time.time()
                
                # System metrics
                memory_info = psutil.virtual_memory()
                cpu_percent = psutil.cpu_percent(interval=1)
                
                # Update internal metrics
                self.gauges['memory_usage_mb'] = memory_info.used / 1024 / 1024
                self.gauges['memory_usage_percent'] = memory_info.percent
                self.gauges['cpu_usage_percent'] = cpu_percent
                self.gauges['uptime_seconds'] = current_time - self.start_time
                
                # Update Prometheus metrics
                self.prom_metrics['memory_usage'].set(memory_info.used)
                self.prom_metrics['cpu_usage'].set(cpu_percent)
                self.prom_metrics['uptime'].set(current_time - self.start_time)
                
                # Store time-series data
                timestamp = int(current_time)
                self.timeseries_metrics['memory_usage'].append((timestamp, memory_info.used))
                self.timeseries_metrics['cpu_usage'].append((timestamp, cpu_percent))
                
                logger.debug(
                    "System metrics collected",
                    memory_mb=f"{memory_info.used / 1024 / 1024:.1f}",
                    cpu_percent=f"{cpu_percent:.1f}",
                    uptime_minutes=f"{(current_time - self.start_time) / 60:.1f}"
                )
                
                time.sleep(self.collection_interval)
                
            except Exception as e:
                logger.error("Failed to collect system metrics", error=str(e))
                time.sleep(self.collection_interval)
    
    def record_request(
        self, 
        method: str, 
        endpoint: str, 
        status_code: int,
        duration: float
    ):
        """Record HTTP request metrics"""
        # Internal metrics
        self.metrics['requests_total'] += 1
        
        if 200 <= status_code < 400:
            self.metrics['requests_successful'] += 1
        else:
            self.metrics['requests_failed'] += 1
        
        self.response_times.append(duration)
        
        # Prometheus metrics
        status_label = 'success' if 200 <= status_code < 400 else 'error'
        self.prom_metrics['requests_total'].labels(
            method=method, 
            endpoint=endpoint, 
            status=status_label
        ).inc()
        
        self.prom_metrics['request_duration'].labels(
            method=method, 
            endpoint=endpoint
        ).observe(duration)
        
        logger.debug(
            "Request recorded",
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            duration=f"{duration:.3f}s"
        )
    
    def record_generation(
        self,
        model: str,
        concept: str,
        quality: str,
        duration: float,
        success: bool,
        cost_estimate: float = 0.0
    ):
        """Record generation request metrics"""
        # Internal metrics
        self.metrics['generation_requests'] += 1
        self.metrics['total_cost_estimate'] += cost_estimate
        
        if success:
            self.metrics['generation_successful'] += 1
        else:
            self.metrics['generation_failed'] += 1
        
        # Prometheus metrics
        self.prom_metrics['generation_requests'].labels(
            model=model,
            concept=concept,
            quality=quality
        ).inc()
        
        self.prom_metrics['generation_duration'].labels(
            model=model,
            concept=concept
        ).observe(duration)
        
        logger.info(
            "Generation recorded",
            model=model,
            concept=concept,
            quality=quality,
            duration=f"{duration:.2f}s",
            success=success,
            cost=f"${cost_estimate:.3f}"
        )
    
    def record_cache_operation(self, operation: str, result: str):
        """Record cache operation metrics"""
        cache_key = f"cache_{operation}_{result}"
        self.metrics[cache_key] += 1
        
        # Prometheus metrics
        self.prom_metrics['cache_operations'].labels(
            operation=operation,
            result=result
        ).inc()
        
        logger.debug("Cache operation recorded", operation=operation, result=result)
    
    def update_active_jobs(self, count: int):
        """Update active jobs gauge"""
        self.gauges['active_jobs'] = count
        self.prom_metrics['active_jobs'].set(count)
    
    def get_summary(self) -> MetricsSummary:
        """Get current metrics summary"""
        # Calculate averages
        avg_response_time = 0.0
        if self.response_times:
            avg_response_time = sum(self.response_times) / len(self.response_times)
        
        # Calculate cache hit rate
        cache_hits = self.metrics.get('cache_hit', 0)
        cache_misses = self.metrics.get('cache_miss', 0)
        cache_total = cache_hits + cache_misses
        cache_hit_rate = (cache_hits / cache_total * 100) if cache_total > 0 else 0.0
        
        return MetricsSummary(
            requests_total=self.metrics['requests_total'],
            requests_successful=self.metrics['requests_successful'],
            requests_failed=self.metrics['requests_failed'],
            avg_response_time=avg_response_time,
            generation_requests=self.metrics['generation_requests'],
            generation_successful=self.metrics['generation_successful'],
            cache_hit_rate=cache_hit_rate,
            total_cost_estimate=self.metrics['total_cost_estimate'],
            uptime_seconds=time.time() - self.start_time,
            memory_usage_mb=self.gauges['memory_usage_mb'],
            cpu_usage_percent=self.gauges['cpu_usage_percent']
        )
    
    def get_detailed_metrics(self) -> Dict[str, Any]:
        """Get detailed metrics for API responses"""
        summary = self.get_summary()
        
        # Recent response times (last 100)
        recent_response_times = list(self.response_times)[-100:]
        
        # Time-series data (last 24 hours)
        current_time = int(time.time())
        time_series = {}
        
        for metric_name, data_points in self.timeseries_metrics.items():
            # Filter last 24 hours
            recent_points = [
                (ts, value) for ts, value in data_points 
                if current_time - ts <= 86400
            ]
            time_series[metric_name] = recent_points
        
        return {
            'summary': summary.__dict__,
            'detailed': {
                'response_times': {
                    'recent': recent_response_times,
                    'percentiles': self._calculate_percentiles(recent_response_times),
                },
                'time_series': time_series,
                'raw_metrics': dict(self.metrics),
                'gauges': dict(self.gauges)
            },
            'health': self._assess_health()
        }
    
    def _calculate_percentiles(self, values: List[float]) -> Dict[str, float]:
        """Calculate response time percentiles"""
        if not values:
            return {}
        
        sorted_values = sorted(values)
        length = len(sorted_values)
        
        return {
            'p50': sorted_values[int(length * 0.5)],
            'p90': sorted_values[int(length * 0.9)],
            'p95': sorted_values[int(length * 0.95)],
            'p99': sorted_values[int(length * 0.99)] if length >= 100 else sorted_values[-1],
        }
    
    def _assess_health(self) -> Dict[str, Any]:
        """Assess service health based on metrics"""
        health = {
            'status': 'healthy',
            'issues': [],
            'warnings': []
        }
        
        # Check error rate
        total_requests = self.metrics.get('requests_total', 0)
        failed_requests = self.metrics.get('requests_failed', 0)
        
        if total_requests > 100:  # Only check if we have enough data
            error_rate = (failed_requests / total_requests) * 100
            
            if error_rate > 10:
                health['status'] = 'unhealthy'
                health['issues'].append(f'High error rate: {error_rate:.1f}%')
            elif error_rate > 5:
                health['warnings'].append(f'Elevated error rate: {error_rate:.1f}%')
        
        # Check response times
        if self.response_times:
            avg_response_time = sum(self.response_times) / len(self.response_times)
            
            if avg_response_time > 10.0:
                health['status'] = 'unhealthy'
                health['issues'].append(f'High response time: {avg_response_time:.2f}s')
            elif avg_response_time > 5.0:
                health['warnings'].append(f'Elevated response time: {avg_response_time:.2f}s')
        
        # Check memory usage
        memory_percent = self.gauges.get('memory_usage_percent', 0)
        if memory_percent > 90:
            health['status'] = 'unhealthy'
            health['issues'].append(f'High memory usage: {memory_percent:.1f}%')
        elif memory_percent > 80:
            health['warnings'].append(f'Elevated memory usage: {memory_percent:.1f}%')
        
        # Check CPU usage
        cpu_percent = self.gauges.get('cpu_usage_percent', 0)
        if cpu_percent > 90:
            health['status'] = 'degraded' if health['status'] == 'healthy' else health['status']
            health['warnings'].append(f'High CPU usage: {cpu_percent:.1f}%')
        
        return health
    
    def get_prometheus_registry(self) -> CollectorRegistry:
        """Get Prometheus metrics registry"""
        return self.registry
    
    def reset_metrics(self):
        """Reset all metrics (useful for testing)"""
        self.metrics.clear()
        self.timeseries_metrics.clear()
        self.gauges.clear()
        self.response_times.clear()
        
        logger.info("All metrics reset")


class AlertManager:
    """Alert management for critical metrics"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
        self.alert_handlers: List[Callable] = []
        self.alert_thresholds = {
            'error_rate_percent': 10.0,
            'avg_response_time_seconds': 10.0,
            'memory_usage_percent': 90.0,
            'cpu_usage_percent': 90.0,
        }
        self.alert_cooldowns = {}  # Track alert cooldowns
        self.cooldown_period = 300  # 5 minutes
        
        logger.info("Alert manager initialized")
    
    def add_alert_handler(self, handler: Callable[[str, Dict[str, Any]], None]):
        """Add alert handler function"""
        self.alert_handlers.append(handler)
        logger.info("Alert handler added")
    
    def check_alerts(self):
        """Check for alert conditions"""
        current_time = time.time()
        summary = self.metrics.get_summary()
        
        # Check error rate
        if summary.requests_total > 100:
            error_rate = (summary.requests_failed / summary.requests_total) * 100
            if error_rate > self.alert_thresholds['error_rate_percent']:
                self._trigger_alert(
                    'high_error_rate',
                    f'Error rate {error_rate:.1f}% exceeds threshold',
                    {'error_rate': error_rate, 'threshold': self.alert_thresholds['error_rate_percent']}
                )
        
        # Check response times
        if (summary.avg_response_time > self.alert_thresholds['avg_response_time_seconds']):
            self._trigger_alert(
                'high_response_time',
                f'Average response time {summary.avg_response_time:.2f}s exceeds threshold',
                {'avg_response_time': summary.avg_response_time}
            )
        
        # Check memory usage
        if summary.memory_usage_mb > 0:  # Only check if we have data
            # Estimate memory percentage (rough calculation)
            total_memory = psutil.virtual_memory().total
            memory_percent = (summary.memory_usage_mb * 1024 * 1024) / total_memory * 100
            
            if memory_percent > self.alert_thresholds['memory_usage_percent']:
                self._trigger_alert(
                    'high_memory_usage',
                    f'Memory usage {memory_percent:.1f}% exceeds threshold',
                    {'memory_usage_percent': memory_percent}
                )
        
        # Check CPU usage
        if summary.cpu_usage_percent > self.alert_thresholds['cpu_usage_percent']:
            self._trigger_alert(
                'high_cpu_usage',
                f'CPU usage {summary.cpu_usage_percent:.1f}% exceeds threshold',
                {'cpu_usage_percent': summary.cpu_usage_percent}
            )
    
    def _trigger_alert(self, alert_type: str, message: str, data: Dict[str, Any]):
        """Trigger alert if not in cooldown period"""
        current_time = time.time()
        last_alert_time = self.alert_cooldowns.get(alert_type, 0)
        
        if current_time - last_alert_time >= self.cooldown_period:
            logger.warning("Alert triggered", alert_type=alert_type, message=message, data=data)
            
            # Call alert handlers
            for handler in self.alert_handlers:
                try:
                    handler(alert_type, {
                        'message': message,
                        'timestamp': datetime.now().isoformat(),
                        'data': data
                    })
                except Exception as e:
                    logger.error("Alert handler failed", handler=handler.__name__, error=str(e))
            
            # Update cooldown
            self.alert_cooldowns[alert_type] = current_time
        else:
            logger.debug(
                "Alert suppressed (cooldown)",
                alert_type=alert_type,
                remaining_cooldown=self.cooldown_period - (current_time - last_alert_time)
            )


# Example alert handlers
def slack_alert_handler(alert_type: str, alert_data: Dict[str, Any]):
    """Example Slack alert handler"""
    logger.info("Slack alert would be sent", alert_type=alert_type, data=alert_data)
    # Implementation would use Slack API

def email_alert_handler(alert_type: str, alert_data: Dict[str, Any]):
    """Example email alert handler"""
    logger.info("Email alert would be sent", alert_type=alert_type, data=alert_data)
    # Implementation would use SMTP