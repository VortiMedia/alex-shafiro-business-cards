#!/usr/bin/env python3
"""
Business Card Generator v4.0 - FastAPI Web Service
Enterprise-ready API with async support, job queuing, and comprehensive monitoring
"""

import os
import sys
import asyncio
import uuid
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
from contextlib import asynccontextmanager

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import structlog
import redis
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Import our core modules
from hybrid.modern_workflow import ModernHybridWorkflow, ModelType, GenerationResult
from cache.redis_cache import GenerationCache
from batch.batch_processor import BatchProcessor
from monitoring.metrics import MetricsCollector

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Prometheus metrics
REQUESTS = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')
GENERATION_REQUESTS = Counter('generation_requests_total', 'Generation requests', ['model', 'concept'])
GENERATION_DURATION = Histogram('generation_duration_seconds', 'Generation duration')

# Pydantic models
class GenerationRequest(BaseModel):
    """Request model for business card generation"""
    concept: str = Field(default="Clinical-Precision", description="Design concept")
    side: str = Field(default="front", description="Card side (front/back)")
    quality: str = Field(default="production", description="Quality level")
    model: Optional[str] = Field(default=None, description="Specific model to use")
    custom_prompt: Optional[str] = Field(default=None, description="Custom prompt override")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class BatchGenerationRequest(BaseModel):
    """Request model for batch generation"""
    concepts: List[str] = Field(default=["Clinical-Precision"], description="Design concepts")
    sides: List[str] = Field(default=["front", "back"], description="Card sides")
    quality: str = Field(default="production", description="Quality level")
    model: Optional[str] = Field(default=None, description="Specific model to use")

class JobStatus(BaseModel):
    """Job status response model"""
    job_id: str
    status: str
    progress: float
    created_at: datetime
    updated_at: datetime
    result_url: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    version: str
    services: Dict[str, str]
    metrics: Dict[str, Any]

# Global variables
app_state = {
    "workflow": None,
    "cache": None,
    "batch_processor": None,
    "metrics": None,
    "jobs": {},
    "redis": None
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Business Card Generator v4.0")
    
    # Initialize services
    try:
        # Initialize workflow engine
        app_state["workflow"] = ModernHybridWorkflow()
        logger.info("Workflow engine initialized")
        
        # Initialize Redis connection
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        app_state["redis"] = redis.from_url(redis_url, decode_responses=True)
        logger.info("Redis connection established", redis_url=redis_url)
        
        # Initialize cache
        app_state["cache"] = GenerationCache(app_state["redis"])
        logger.info("Generation cache initialized")
        
        # Initialize batch processor
        app_state["batch_processor"] = BatchProcessor(app_state["workflow"])
        logger.info("Batch processor initialized")
        
        # Initialize metrics collector
        app_state["metrics"] = MetricsCollector()
        logger.info("Metrics collector initialized")
        
        logger.info("All services initialized successfully")
        
    except Exception as e:
        logger.error("Failed to initialize services", error=str(e))
        raise
    
    yield
    
    # Cleanup
    logger.info("Shutting down Business Card Generator v4.0")
    if app_state["redis"]:
        app_state["redis"].close()

# Create FastAPI app
app = FastAPI(
    title="Business Card Generator API",
    description="AI-powered business card generation with dual model support",
    version="4.0.0",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Security (optional JWT bearer token)
security = HTTPBearer(auto_error=False)

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token (optional authentication)"""
    if not credentials:
        return None
    
    # In production, implement proper JWT verification
    # For now, accept any bearer token for demonstration
    return {"user_id": "demo_user"}

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with metrics"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    REQUESTS.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(process_time)
    
    logger.info(
        "Request processed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=process_time
    )
    
    return response

# Root endpoint - serve web interface
@app.get("/", response_class=HTMLResponse)
async def web_interface(request: Request):
    """Serve the main web interface"""
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "title": "Business Card Generator",
            "version": "4.0.0"
        }
    )

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check"""
    try:
        # Test Redis connection
        redis_status = "healthy" if app_state["redis"].ping() else "unhealthy"
        
        # Test workflow engine
        workflow_status = "healthy" if app_state["workflow"] else "unhealthy"
        
        # Collect metrics
        metrics = app_state["metrics"].get_summary() if app_state["metrics"] else {}
        
        return HealthResponse(
            status="healthy" if all([
                redis_status == "healthy",
                workflow_status == "healthy"
            ]) else "degraded",
            timestamp=datetime.now(),
            version="4.0.0",
            services={
                "redis": redis_status,
                "workflow": workflow_status,
                "cache": "healthy" if app_state["cache"] else "unhealthy",
                "batch_processor": "healthy" if app_state["batch_processor"] else "unhealthy"
            },
            metrics=metrics
        )
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service unhealthy")

# Generate single business card
@app.post("/api/generate")
async def generate_card(
    request: GenerationRequest,
    background_tasks: BackgroundTasks,
    user: Optional[Dict] = Depends(verify_token)
):
    """Generate a single business card"""
    job_id = str(uuid.uuid4())
    
    logger.info(
        "Generation request received",
        job_id=job_id,
        concept=request.concept,
        side=request.side,
        quality=request.quality,
        user_id=user.get("user_id") if user else None
    )
    
    # Record metrics
    model_name = request.model or "auto"
    GENERATION_REQUESTS.labels(model=model_name, concept=request.concept).inc()
    
    # Create job entry
    job = {
        "id": job_id,
        "status": "queued",
        "progress": 0.0,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "request": request.dict(),
        "user_id": user.get("user_id") if user else None
    }
    
    app_state["jobs"][job_id] = job
    
    # Queue background task
    background_tasks.add_task(
        process_generation_job, 
        job_id, 
        request
    )
    
    return {
        "job_id": job_id,
        "status": "queued",
        "estimated_completion": "30-60 seconds"
    }

# Generate batch of business cards
@app.post("/api/generate/batch")
async def generate_batch(
    request: BatchGenerationRequest,
    background_tasks: BackgroundTasks,
    user: Optional[Dict] = Depends(verify_token)
):
    """Generate multiple business cards in batch"""
    job_id = str(uuid.uuid4())
    
    logger.info(
        "Batch generation request received",
        job_id=job_id,
        concepts=request.concepts,
        sides=request.sides,
        quality=request.quality,
        user_id=user.get("user_id") if user else None
    )
    
    # Create job entry
    job = {
        "id": job_id,
        "status": "queued",
        "progress": 0.0,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "request": request.dict(),
        "user_id": user.get("user_id") if user else None,
        "type": "batch"
    }
    
    app_state["jobs"][job_id] = job
    
    # Queue background task
    background_tasks.add_task(
        process_batch_job,
        job_id,
        request
    )
    
    total_cards = len(request.concepts) * len(request.sides)
    
    return {
        "job_id": job_id,
        "status": "queued",
        "total_cards": total_cards,
        "estimated_completion": f"{total_cards * 30}-{total_cards * 60} seconds"
    }

# Check job status
@app.get("/api/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get generation job status"""
    if job_id not in app_state["jobs"]:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = app_state["jobs"][job_id]
    
    return JobStatus(
        job_id=job["id"],
        status=job["status"],
        progress=job["progress"],
        created_at=job["created_at"],
        updated_at=job["updated_at"],
        result_url=job.get("result_url"),
        error_message=job.get("error_message"),
        metadata=job.get("metadata")
    )

# List user's jobs
@app.get("/api/jobs")
async def list_jobs(
    limit: int = 10,
    offset: int = 0,
    user: Optional[Dict] = Depends(verify_token)
):
    """List generation jobs for user"""
    user_id = user.get("user_id") if user else None
    
    # Filter jobs by user (if authenticated)
    jobs = [
        job for job in app_state["jobs"].values()
        if not user_id or job.get("user_id") == user_id
    ]
    
    # Sort by creation time (newest first)
    jobs = sorted(jobs, key=lambda x: x["created_at"], reverse=True)
    
    # Paginate
    total = len(jobs)
    jobs = jobs[offset:offset + limit]
    
    return {
        "jobs": jobs,
        "total": total,
        "limit": limit,
        "offset": offset
    }

# Download generated file
@app.get("/api/download/{job_id}")
async def download_file(job_id: str):
    """Download generated business card file"""
    if job_id not in app_state["jobs"]:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = app_state["jobs"][job_id]
    
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job not completed")
    
    if not job.get("result_url"):
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = Path(job["result_url"])
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="image/png"
    )

# Prometheus metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

# Background task functions
async def process_generation_job(job_id: str, request: GenerationRequest):
    """Process single generation job"""
    start_time = time.time()
    
    try:
        # Update job status
        job = app_state["jobs"][job_id]
        job["status"] = "processing"
        job["progress"] = 10.0
        job["updated_at"] = datetime.now()
        
        logger.info("Starting generation", job_id=job_id)
        
        # Check cache first
        cache_key = f"{request.concept}:{request.side}:{request.quality}:{request.model}"
        cached_result = app_state["cache"].get_cached(cache_key)
        
        if cached_result:
            logger.info("Using cached result", job_id=job_id, cache_key=cache_key)
            job["result_url"] = cached_result.filepath
            job["status"] = "completed"
            job["progress"] = 100.0
            job["updated_at"] = datetime.now()
            return
        
        # Update progress
        job["progress"] = 30.0
        job["updated_at"] = datetime.now()
        
        # Determine model
        model = ModelType.AUTO
        if request.model:
            model = ModelType(request.model)
        
        # Generate card
        result = app_state["workflow"].generate_card(
            concept=request.concept,
            side=request.side,
            model=model,
            quality=request.quality
        )
        
        # Update progress
        job["progress"] = 80.0
        job["updated_at"] = datetime.now()
        
        if result.success:
            # Cache result
            app_state["cache"].cache_result(cache_key, result)
            
            # Update job
            job["status"] = "completed"
            job["progress"] = 100.0
            job["result_url"] = result.filepath
            job["metadata"] = {
                "model_used": result.model_used,
                "cost_estimate": result.cost_estimate,
                "processing_time": result.processing_time
            }
            
            logger.info(
                "Generation completed successfully",
                job_id=job_id,
                filepath=result.filepath,
                model=result.model_used,
                processing_time=result.processing_time
            )
            
        else:
            job["status"] = "failed"
            job["error_message"] = result.error_message
            
            logger.error(
                "Generation failed",
                job_id=job_id,
                error=result.error_message
            )
        
        job["updated_at"] = datetime.now()
        
        # Record metrics
        duration = time.time() - start_time
        GENERATION_DURATION.observe(duration)
        
    except Exception as e:
        logger.error("Job processing failed", job_id=job_id, error=str(e))
        
        job = app_state["jobs"][job_id]
        job["status"] = "failed"
        job["error_message"] = str(e)
        job["updated_at"] = datetime.now()

async def process_batch_job(job_id: str, request: BatchGenerationRequest):
    """Process batch generation job"""
    try:
        # Update job status
        job = app_state["jobs"][job_id]
        job["status"] = "processing"
        job["progress"] = 0.0
        job["updated_at"] = datetime.now()
        
        logger.info("Starting batch generation", job_id=job_id)
        
        # Use batch processor
        results = await app_state["batch_processor"].process_batch(
            concepts=request.concepts,
            sides=request.sides,
            quality=request.quality,
            model=request.model,
            progress_callback=lambda p: update_job_progress(job_id, p)
        )
        
        # Update job with results
        job["status"] = "completed"
        job["progress"] = 100.0
        job["results"] = [
            {
                "concept": r.concept,
                "side": r.side,
                "success": r.success,
                "filepath": r.filepath,
                "error": r.error_message
            }
            for r in results
        ]
        job["updated_at"] = datetime.now()
        
        logger.info(
            "Batch generation completed",
            job_id=job_id,
            total_results=len(results),
            successful=sum(1 for r in results if r.success)
        )
        
    except Exception as e:
        logger.error("Batch job processing failed", job_id=job_id, error=str(e))
        
        job = app_state["jobs"][job_id]
        job["status"] = "failed"
        job["error_message"] = str(e)
        job["updated_at"] = datetime.now()

def update_job_progress(job_id: str, progress: float):
    """Update job progress"""
    if job_id in app_state["jobs"]:
        app_state["jobs"][job_id]["progress"] = progress
        app_state["jobs"][job_id]["updated_at"] = datetime.now()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )