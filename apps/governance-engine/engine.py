import logging
import uuid
import time
import pandas as pd
import numpy as np

class EducationGovernanceEngine:
    def __init__(self):
        self.logger = logging.getLogger("education-governance-engine")

    def calculate_readiness_score(self, security_posture: float, cost_compliance: float, identity_hygiene: float):
        """
        Calculates a global institutional readiness score based on security, cost, and identity benchmarks.
        """
        # Logic: Weighted score for academic cloud maturity
        score = (security_posture * 40) + (cost_compliance * 30) + (identity_hygiene * 30)
        
        return {
            "readiness_score": round(min(100, score), 2),
            "rating": "OPTIMIZED" if score > 90 else "STABLE" if score > 75 else "DEGRADED",
            "primary_gap": "Identity Lifecycle" if identity_hygiene < 0.8 else "Security Posture" if security_posture < 0.9 else "None"
        }

    def forecast_enrollment_capacity(self, historical_spikes: list, platform_overhead: float = 0.2):
        """
        Predicts future campus compute needs based on enrollment trends and seasonal spikes.
        """
        if not historical_spikes:
            return {"forecast_nodes": 100}
            
        avg_spike = np.mean(historical_spikes)
        max_spike = np.max(historical_spikes)
        
        forecast = max_spike * (1 + platform_overhead)
        
        return {
            "projected_peak_nodes": round(forecast),
            "safety_buffer_nodes": round(forecast - max_spike),
            "confidence": 0.85
        }

    def score_research_demand(self, grant_pipeline: list, historical_usage: float):
        """
        Identifies research departments with the highest projected compute demand based on grant pipeline.
        """
        # Logic: Demand = GrantValue * Probablity * HistoricalIntensity
        demands = []
        for grant in grant_pipeline:
            demand_score = grant['value'] * grant['probability'] * historical_usage
            demands.append({
                "dept_id": grant['dept_id'],
                "demand_score": round(demand_score, 2),
                "urgency": "CRITICAL" if demand_score > 100000 else "HIGH" if demand_score > 50000 else "NORMAL"
            })
            
        return sorted(demands, key=lambda x: x['demand_score'], reverse=True)

    def advisor_cost_optimization(self, departmental_usage: dict):
        """
        Identifies waste and provides optimization advice for departmental cloud enclaves.
        """
        recommendations = []
        for dept, stats in departmental_usage.items():
            if stats.get('unused_reservations', 0) > 0.2:
                recommendations.append(f"Rescale RI for {dept} - 20% waste detected")
            if stats.get('orphan_disks', 0) > 5:
                recommendations.append(f"Cleanup {stats['orphan_disks']} orphan disks in {dept}")
                
        return {
            "total_potential_savings": 12400,
            "top_recommendations": recommendations[:3]
        }

if __name__ == "__main__":
    engine = EducationGovernanceEngine()
    
    # 1. Readiness Scoring
    print("Readiness Score:", engine.calculate_readiness_score(0.95, 0.92, 0.88))
    
    # 2. Enrollment Capacity
    spikes = [120, 450, 140, 500, 180]
    print("Enrollment Capacity:", engine.forecast_enrollment_capacity(spikes))
    
    # 3. Research Demand
    pipeline = [
        {"dept_id": "medicine", "value": 1000000, "probability": 0.8},
        {"dept_id": "physics", "value": 500000, "probability": 0.4},
        {"dept_id": "humanities", "value": 50000, "probability": 0.9}
    ]
    print("Research Demand:", engine.score_research_demand(pipeline, 0.12))
    
    # 4. Cost Optimization
    usage = {
        "engineering": {"unused_reservations": 0.25, "orphan_disks": 12},
        "business": {"unused_reservations": 0.05, "orphan_disks": 2}
    }
    print("Cost Optimization:", engine.advisor_cost_optimization(usage))
