#!/usr/bin/env python3
"""
Business Card Generator v4.0 - Simplified FastAPI MVP
Without Redis/complex dependencies for immediate deployment
"""

import os
import sys
import uuid
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import our core modules
from hybrid.modern_workflow import ModernHybridWorkflow, ModelType, GenerationResult

# Pydantic models
class GenerationRequest(BaseModel):
    """Request model for business card generation"""
    concept: str = Field(default="Clinical-Precision", description="Design concept")
    side: str = Field(default="front", description="Card side (front/back)")
    quality: str = Field(default="production", description="Quality level")
    model: Optional[str] = Field(default=None, description="Specific model to use")

class BatchGenerationRequest(BaseModel):
    """Request model for batch generation"""
    concepts: list[str] = Field(default=["Clinical-Precision"], description="Design concepts")
    sides: list[str] = Field(default=["front", "back"], description="Card sides")
    quality: str = Field(default="production", description="Quality level")

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

# Global state (simplified - no Redis for MVP)
app_state = {
    "workflow": None,
    "jobs": {},
    "start_time": time.time()
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    print("🚀 Starting Business Card Generator MVP...")
    
    try:
        # Initialize workflow engine
        app_state["workflow"] = ModernHybridWorkflow()
        print("✅ Workflow engine initialized")
        
        print("✅ All services initialized successfully")
        
    except Exception as e:
        print(f"❌ Failed to initialize services: {e}")
        raise
    
    yield
    
    # Cleanup
    print("🔄 Shutting down Business Card Generator...")

# Create FastAPI app
app = FastAPI(
    title="Business Card Generator MVP",
    description="AI-powered business card generation",
    version="4.0.0-mvp",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Root endpoint - serve web interface
@app.get("/")
async def web_interface(request: Request):
    """Serve the main web interface"""
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "title": "Business Card Generator",
            "version": "4.0.0-mvp"
        }
    )

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check"""
    try:
        workflow_status = "healthy" if app_state["workflow"] else "unhealthy"
        
        return HealthResponse(
            status="healthy" if workflow_status == "healthy" else "degraded",
            timestamp=datetime.now(),
            version="4.0.0-mvp",
            services={
                "workflow": workflow_status,
                "cache": "disabled",  # Simplified for MVP
                "batch_processor": "healthy"
            }
        )
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

# Generate single business card
@app.post("/api/generate")
async def generate_card(
    request: GenerationRequest,
    background_tasks: BackgroundTasks
):
    """Generate a single business card"""
    job_id = str(uuid.uuid4())
    
    print(f"🎨 Generation request: {request.concept} {request.side} ({request.quality})")
    
    # Create job entry
    job = {
        "id": job_id,
        "status": "queued",
        "progress": 0.0,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "request": request.dict()
    }
    
    app_state["jobs"][job_id] = job
    
    # Queue background task
    background_tasks.add_task(process_generation_job, job_id, request)
    
    return {
        "job_id": job_id,
        "status": "queued",
        "estimated_completion": "30-60 seconds"
    }

# Generate batch of business cards
@app.post("/api/generate/batch")
async def generate_batch(
    request: BatchGenerationRequest,
    background_tasks: BackgroundTasks
):
    """Generate multiple business cards in batch"""
    job_id = str(uuid.uuid4())
    
    print(f"🚀 Batch request: {len(request.concepts)} concepts x {len(request.sides)} sides")
    
    # Create job entry
    job = {
        "id": job_id,
        "status": "queued",
        "progress": 0.0,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "request": request.dict(),
        "type": "batch"
    }
    
    app_state["jobs"][job_id] = job
    
    # Queue background task
    background_tasks.add_task(process_batch_job, job_id, request)
    
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
        
        print(f"🎨 Processing job {job_id}")
        
        # Update progress
        job["progress"] = 30.0
        job["updated_at"] = datetime.now()
        
        # Determine model
        model = ModelType.AUTO
        if request.model:
            try:
                model = ModelType(request.model)
            except ValueError:
                print(f"⚠️ Invalid model {request.model}, using AUTO")
        
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
            # Update job
            job["status"] = "completed"
            job["progress"] = 100.0
            job["result_url"] = result.filepath
            job["metadata"] = {
                "model_used": result.model_used,
                "cost_estimate": result.cost_estimate,
                "processing_time": result.processing_time
            }
            
            print(f"✅ Job {job_id} completed: {result.filepath}")
            
        else:
            job["status"] = "failed"
            job["error_message"] = result.error_message
            print(f"❌ Job {job_id} failed: {result.error_message}")
        
        job["updated_at"] = datetime.now()
        
    except Exception as e:
        print(f"❌ Job {job_id} processing failed: {e}")
        
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
        
        print(f"🚀 Processing batch job {job_id}")
        
        results = []
        total_tasks = len(request.concepts) * len(request.sides)
        completed = 0
        
        for concept in request.concepts:
            for side in request.sides:
                # Generate single card
                result = app_state["workflow"].generate_card(
                    concept=concept,
                    side=side,
                    model=ModelType.AUTO,
                    quality=request.quality
                )
                
                results.append({
                    "concept": concept,
                    "side": side,
                    "success": result.success,
                    "filepath": result.filepath,
                    "error": result.error_message
                })
                
                completed += 1
                job["progress"] = (completed / total_tasks) * 100
                job["updated_at"] = datetime.now()
                
                print(f"📄 Batch progress: {completed}/{total_tasks}")
        
        # Update job with results
        job["status"] = "completed"
        job["progress"] = 100.0
        job["results"] = results
        job["updated_at"] = datetime.now()
        
        successful = sum(1 for r in results if r["success"])
        print(f"✅ Batch job {job_id} completed: {successful}/{len(results)} successful")
        
    except Exception as e:
        print(f"❌ Batch job {job_id} failed: {e}")
        
        job = app_state["jobs"][job_id]
        job["status"] = "failed"
        job["error_message"] = str(e)
        job["updated_at"] = datetime.now()

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Business Card Generator MVP...")
    print("🌐 Web interface: http://localhost:8000")
    print("📚 API docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "simple_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )