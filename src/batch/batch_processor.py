#!/usr/bin/env python3
"""
Batch Processing System for Business Card Generator

Handles parallel generation of multiple business cards with intelligent
load balancing, progress tracking, and error handling.
"""

import asyncio
import time
from typing import List, Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import structlog

from ..hybrid.modern_workflow import ModernHybridWorkflow, ModelType, GenerationResult

logger = structlog.get_logger(__name__)

@dataclass
class BatchRequest:
    """Individual request within a batch"""
    concept: str
    side: str
    quality: str = "production"
    model: Optional[str] = None
    priority: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass 
class BatchResult:
    """Result from batch processing"""
    concept: str
    side: str
    success: bool
    filepath: Optional[str] = None
    model_used: Optional[str] = None
    processing_time: float = 0.0
    cost_estimate: float = 0.0
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class BatchProcessor:
    """Parallel batch processing for business card generation"""
    
    def __init__(
        self, 
        workflow: ModernHybridWorkflow,
        max_workers: int = 4,
        max_concurrent_per_model: int = 2
    ):
        """
        Initialize batch processor
        
        Args:
            workflow: ModernHybridWorkflow instance
            max_workers: Maximum concurrent workers
            max_concurrent_per_model: Max concurrent requests per AI model
        """
        self.workflow = workflow
        self.max_workers = max_workers
        self.max_concurrent_per_model = max_concurrent_per_model
        
        # Track active requests per model to avoid rate limits
        self.active_requests = {
            "gpt-image-1": 0,
            "gemini-2.5-flash-image-preview": 0
        }
        
        logger.info(
            "Batch processor initialized",
            max_workers=max_workers,
            max_concurrent_per_model=max_concurrent_per_model
        )
    
    async def process_batch(
        self,
        concepts: List[str],
        sides: List[str],
        quality: str = "production",
        model: Optional[str] = None,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> List[BatchResult]:
        """
        Process a batch of generation requests
        
        Args:
            concepts: List of design concepts to generate
            sides: List of card sides ("front", "back")
            quality: Quality level for all cards
            model: Specific model to use (optional)
            progress_callback: Callback for progress updates
            
        Returns:
            List of BatchResult objects
        """
        # Create batch requests
        requests = []
        for concept in concepts:
            for side in sides:
                requests.append(BatchRequest(
                    concept=concept,
                    side=side,
                    quality=quality,
                    model=model,
                    priority=self._calculate_priority(concept, side, quality)
                ))
        
        logger.info(
            "Starting batch processing",
            total_requests=len(requests),
            concepts=concepts,
            sides=sides,
            quality=quality
        )
        
        return await self._process_requests(requests, progress_callback)
    
    async def process_custom_batch(
        self,
        requests: List[BatchRequest],
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> List[BatchResult]:
        """
        Process a custom batch of requests with individual settings
        
        Args:
            requests: List of BatchRequest objects
            progress_callback: Callback for progress updates
            
        Returns:
            List of BatchResult objects
        """
        logger.info("Starting custom batch processing", total_requests=len(requests))
        return await self._process_requests(requests, progress_callback)
    
    async def _process_requests(
        self,
        requests: List[BatchRequest],
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> List[BatchResult]:
        """Internal method to process batch requests"""
        start_time = time.time()
        results = []
        completed = 0
        
        # Sort requests by priority (higher first)
        requests.sort(key=lambda r: r.priority, reverse=True)
        
        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_request = {
                executor.submit(self._process_single_request, req): req
                for req in requests
            }
            
            # Process completed tasks
            for future in as_completed(future_to_request):
                request = future_to_request[future]
                
                try:
                    result = future.result()
                    results.append(result)
                    
                    logger.debug(
                        "Request completed",
                        concept=request.concept,
                        side=request.side,
                        success=result.success
                    )
                    
                except Exception as e:
                    logger.error(
                        "Request failed",
                        concept=request.concept,
                        side=request.side,
                        error=str(e)
                    )
                    
                    # Create error result
                    results.append(BatchResult(
                        concept=request.concept,
                        side=request.side,
                        success=False,
                        error_message=str(e)
                    ))
                
                # Update progress
                completed += 1
                progress = completed / len(requests) * 100.0
                
                if progress_callback:
                    progress_callback(progress)
                
                logger.debug(
                    "Batch progress update",
                    completed=completed,
                    total=len(requests),
                    progress=f"{progress:.1f}%"
                )
        
        # Calculate batch statistics
        total_time = time.time() - start_time
        successful = sum(1 for r in results if r.success)
        total_cost = sum(r.cost_estimate for r in results)
        
        logger.info(
            "Batch processing completed",
            total_requests=len(requests),
            successful=successful,
            failed=len(requests) - successful,
            total_time=f"{total_time:.2f}s",
            total_cost=f"${total_cost:.3f}",
            avg_time_per_card=f"{total_time / len(requests):.2f}s"
        )
        
        return results
    
    def _process_single_request(self, request: BatchRequest) -> BatchResult:
        """Process a single generation request (synchronous)"""
        start_time = time.time()
        
        try:
            # Determine model
            model = ModelType.AUTO
            if request.model:
                try:
                    model = ModelType(request.model)
                except ValueError:
                    logger.warning(
                        "Invalid model specified, using AUTO",
                        requested_model=request.model
                    )
            
            # Rate limiting check
            model_name = model.value if model != ModelType.AUTO else "auto"
            if not self._check_rate_limit(model_name):
                logger.warning(
                    "Rate limit reached, waiting",
                    model=model_name,
                    concept=request.concept,
                    side=request.side
                )
                time.sleep(1)  # Brief wait
            
            # Increment active requests counter
            self._increment_active_requests(model_name)
            
            try:
                # Generate card
                result = self.workflow.generate_card(
                    concept=request.concept,
                    side=request.side,
                    model=model,
                    quality=request.quality
                )
                
                processing_time = time.time() - start_time
                
                # Create batch result
                batch_result = BatchResult(
                    concept=request.concept,
                    side=request.side,
                    success=result.success,
                    filepath=result.filepath,
                    model_used=result.model_used,
                    processing_time=processing_time,
                    cost_estimate=result.cost_estimate,
                    error_message=result.error_message,
                    metadata={
                        **request.metadata,
                        "priority": request.priority,
                        "queue_time": start_time - time.time() + processing_time
                    }
                )
                
                return batch_result
                
            finally:
                # Decrement active requests counter
                self._decrement_active_requests(model_name)
        
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(
                "Single request processing failed",
                concept=request.concept,
                side=request.side,
                error=str(e),
                processing_time=processing_time
            )
            
            return BatchResult(
                concept=request.concept,
                side=request.side,
                success=False,
                processing_time=processing_time,
                error_message=str(e),
                metadata=request.metadata
            )
    
    def _calculate_priority(self, concept: str, side: str, quality: str) -> int:
        """Calculate request priority for optimal processing order"""
        priority = 1
        
        # Higher priority for production quality
        if quality == "production":
            priority += 2
        elif quality == "review":
            priority += 1
        
        # Slightly higher priority for front cards (often needed first)
        if side == "front":
            priority += 1
        
        # Concept-based priority (if needed)
        concept_priorities = {
            "Clinical-Precision": 3,
            "Athletic-Edge": 2,
            "Luxury-Wellness": 1
        }
        priority += concept_priorities.get(concept, 0)
        
        return priority
    
    def _check_rate_limit(self, model_name: str) -> bool:
        """Check if we can make another request to the specified model"""
        # Map model names to rate limit keys
        rate_limit_key = model_name
        if "gpt" in model_name.lower():
            rate_limit_key = "gpt-image-1"
        elif "gemini" in model_name.lower():
            rate_limit_key = "gemini-2.5-flash-image-preview"
        
        current_active = self.active_requests.get(rate_limit_key, 0)
        return current_active < self.max_concurrent_per_model
    
    def _increment_active_requests(self, model_name: str):
        """Increment active request counter for model"""
        rate_limit_key = model_name
        if "gpt" in model_name.lower():
            rate_limit_key = "gpt-image-1"
        elif "gemini" in model_name.lower():
            rate_limit_key = "gemini-2.5-flash-image-preview"
        
        if rate_limit_key in self.active_requests:
            self.active_requests[rate_limit_key] += 1
    
    def _decrement_active_requests(self, model_name: str):
        """Decrement active request counter for model"""
        rate_limit_key = model_name
        if "gpt" in model_name.lower():
            rate_limit_key = "gpt-image-1"
        elif "gemini" in model_name.lower():
            rate_limit_key = "gemini-2.5-flash-image-preview"
        
        if rate_limit_key in self.active_requests:
            self.active_requests[rate_limit_key] = max(0, self.active_requests[rate_limit_key] - 1)


class BatchJobManager:
    """Manages multiple batch processing jobs with queuing"""
    
    def __init__(self, batch_processor: BatchProcessor):
        self.batch_processor = batch_processor
        self.active_jobs = {}
        self.job_queue = asyncio.Queue()
        self.max_concurrent_jobs = 2
        self.active_job_count = 0
        
        logger.info("Batch job manager initialized", max_concurrent_jobs=self.max_concurrent_jobs)
    
    async def submit_batch_job(
        self,
        job_id: str,
        requests: List[BatchRequest],
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Submit a batch job for processing"""
        
        job = {
            "id": job_id,
            "requests": requests,
            "progress_callback": progress_callback,
            "status": "queued",
            "created_at": datetime.now(),
            "results": None
        }
        
        self.active_jobs[job_id] = job
        await self.job_queue.put(job)
        
        # Start job processing if not at capacity
        if self.active_job_count < self.max_concurrent_jobs:
            asyncio.create_task(self._process_job_queue())
        
        logger.info("Batch job submitted", job_id=job_id, num_requests=len(requests))
        return job_id
    
    async def _process_job_queue(self):
        """Process jobs from the queue"""
        if self.active_job_count >= self.max_concurrent_jobs:
            return
        
        self.active_job_count += 1
        
        try:
            while True:
                try:
                    # Get job with timeout
                    job = await asyncio.wait_for(self.job_queue.get(), timeout=1.0)
                    
                    job["status"] = "processing"
                    job["started_at"] = datetime.now()
                    
                    logger.info("Processing batch job", job_id=job["id"])
                    
                    # Process the batch
                    results = await self.batch_processor.process_custom_batch(
                        job["requests"],
                        job["progress_callback"]
                    )
                    
                    # Update job status
                    job["status"] = "completed"
                    job["completed_at"] = datetime.now()
                    job["results"] = results
                    
                    logger.info(
                        "Batch job completed",
                        job_id=job["id"],
                        successful=sum(1 for r in results if r.success),
                        total=len(results)
                    )
                    
                except asyncio.TimeoutError:
                    # No more jobs in queue
                    break
                    
                except Exception as e:
                    if "job" in locals():
                        job["status"] = "failed"
                        job["error"] = str(e)
                        job["completed_at"] = datetime.now()
                    
                    logger.error("Batch job processing failed", error=str(e))
                
        finally:
            self.active_job_count -= 1
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a batch job"""
        return self.active_jobs.get(job_id)
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a batch job (if not started)"""
        job = self.active_jobs.get(job_id)
        if job and job["status"] == "queued":
            job["status"] = "cancelled"
            job["cancelled_at"] = datetime.now()
            logger.info("Batch job cancelled", job_id=job_id)
            return True
        
        return False
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get overall queue status"""
        queued = sum(1 for job in self.active_jobs.values() if job["status"] == "queued")
        processing = sum(1 for job in self.active_jobs.values() if job["status"] == "processing")
        completed = sum(1 for job in self.active_jobs.values() if job["status"] == "completed")
        failed = sum(1 for job in self.active_jobs.values() if job["status"] == "failed")
        
        return {
            "queue_size": self.job_queue.qsize(),
            "active_jobs": self.active_job_count,
            "max_concurrent": self.max_concurrent_jobs,
            "job_stats": {
                "queued": queued,
                "processing": processing,
                "completed": completed,
                "failed": failed,
                "total": len(self.active_jobs)
            }
        }