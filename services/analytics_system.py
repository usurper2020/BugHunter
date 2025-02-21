"""
Analytics system for the BugHunter application.
Handles data analysis, metrics tracking, and reporting insights.
"""

import logging
import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text

@dataclass
class AnalyticsMetric:
    """Represents an analytics metric"""
    name: str
    value: float
    category: str
    timestamp: str
    metadata: Dict[str, Any]

@dataclass
class AnalyticsReport:
    """Represents an analytics report"""
    metrics: List[AnalyticsMetric]
    insights: List[Dict[str, Any]]
    period: str
    generated_at: str

class AnalyticsSystem:
    """Manages analytics and metrics tracking"""
    
    def __init__(self):
        self.logger = logging.getLogger('BugHunter.AnalyticsSystem')
        self.data_dir = Path('data/analytics')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.config: Dict[str, Any] = {}
        self.db_engine = None
        self.initialized = False
    
    def initialize(self) -> bool:
        """Initialize analytics system"""
        try:
            # Load configuration
            config_file = Path('config/analytics_config.json')
            if config_file.exists():
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
            
            # Initialize database connection
            db_url = self.config.get('database_url')
            if not db_url:
                raise ValueError("Database URL not configured")
            
            self.db_engine = create_engine(db_url)
            
            # Set up plotting style
            plt.style.use('seaborn')
            
            self.initialized = True
            self.logger.info("Analytics system initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Analytics system initialization failed: {str(e)}")
            return False
    
    def track_metric(self, metric: AnalyticsMetric) -> bool:
        """Track a new analytics metric"""
        try:
            # Save metric to database
            with self.db_engine.connect() as conn:
                conn.execute(
                    text("""
                    INSERT INTO analytics_metrics 
                    (name, value, category, timestamp, metadata)
                    VALUES (:name, :value, :category, :timestamp, :metadata)
                    """),
                    {
                        'name': metric.name,
                        'value': metric.value,
                        'category': metric.category,
                        'timestamp': metric.timestamp,
                        'metadata': json.dumps(metric.metadata)
                    }
                )
                conn.commit()
            
            self.logger.info(f"Tracked metric: {metric.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to track metric: {str(e)}")
            return False
    
    def generate_report(self, period: str = 'daily') -> Optional[AnalyticsReport]:
        """Generate analytics report for specified period"""
        try:
            # Calculate date range
            end_date = datetime.now()
            if period == 'daily':
                start_date = end_date - timedelta(days=1)
            elif period == 'weekly':
                start_date = end_date - timedelta(weeks=1)
            elif period == 'monthly':
                start_date = end_date - timedelta(days=30)
            else:
                raise ValueError(f"Invalid period: {period}")
            
            # Fetch metrics from database
            metrics = self._fetch_metrics(start_date, end_date)
            
            # Generate insights
            insights = self._generate_insights(metrics)
            
            # Create visualizations
            self._create_visualizations(metrics, period)
            
            report = AnalyticsReport(
                metrics=metrics,
                insights=insights,
                period=period,
                generated_at=datetime.now().isoformat()
            )
            
            # Save report
            self._save_report(report)
            
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate report: {str(e)}")
            return None
    
    def _fetch_metrics(self, start_date: datetime, end_date: datetime) -> List[AnalyticsMetric]:
        """Fetch metrics from database"""
        try:
            query = text("""
                SELECT name, value, category, timestamp, metadata
                FROM analytics_metrics
                WHERE timestamp BETWEEN :start_date AND :end_date
                ORDER BY timestamp DESC
            """)
            
            with self.db_engine.connect() as conn:
                result = conn.execute(
                    query,
                    {'start_date': start_date.isoformat(), 'end_date': end_date.isoformat()}
                )
                
                metrics = []
                for row in result:
                    metrics.append(AnalyticsMetric(
                        name=row.name,
                        value=row.value,
                        category=row.category,
                        timestamp=row.timestamp,
                        metadata=json.loads(row.metadata)
                    ))
                
                return metrics
                
        except Exception as e:
            self.logger.error(f"Failed to fetch metrics: {str(e)}")
            raise
    
    def _generate_insights(self, metrics: List[AnalyticsMetric]) -> List[Dict[str, Any]]:
        """Generate insights from metrics"""
        insights = []
        try:
            # Convert metrics to DataFrame for analysis
            df = pd.DataFrame([{
                'name': m.name,
                'value': m.value,
                'category': m.category,
                'timestamp': pd.to_datetime(m.timestamp)
            } for m in metrics])
            
            # Group by category and calculate statistics
            for category in df['category'].unique():
                category_df = df[df['category'] == category]
                
                # Calculate basic statistics
                stats = category_df.groupby('name')['value'].agg([
                    'mean', 'std', 'min', 'max', 'count'
                ]).round(2)
                
                # Detect anomalies (values outside 2 standard deviations)
                for name in category_df['name'].unique():
                    name_df = category_df[category_df['name'] == name]
                    mean = name_df['value'].mean()
                    std = name_df['value'].std()
                    
                    anomalies = name_df[
                        (name_df['value'] > mean + 2*std) |
                        (name_df['value'] < mean - 2*std)
                    ]
                    
                    if not anomalies.empty:
                        insights.append({
                            'type': 'anomaly',
                            'category': category,
                            'metric': name,
                            'details': f"Found {len(anomalies)} anomalous values"
                        })
                
                # Detect trends
                for name in category_df['name'].unique():
                    name_df = category_df[category_df['name'] == name].sort_values('timestamp')
                    if len(name_df) >= 3:
                        correlation = name_df['value'].corr(pd.Series(range(len(name_df))))
                        if abs(correlation) > 0.7:
                            trend = 'increasing' if correlation > 0 else 'decreasing'
                            insights.append({
                                'type': 'trend',
                                'category': category,
                                'metric': name,
                                'details': f"Strong {trend} trend detected"
                            })
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Failed to generate insights: {str(e)}")
            return []
    
    def _create_visualizations(self, metrics: List[AnalyticsMetric], period: str):
        """Create visualization plots"""
        try:
            # Convert metrics to DataFrame
            df = pd.DataFrame([{
                'name': m.name,
                'value': m.value,
                'category': m.category,
                'timestamp': pd.to_datetime(m.timestamp)
            } for m in metrics])
            
            # Create time series plots for each category
            for category in df['category'].unique():
                category_df = df[df['category'] == category]
                
                plt.figure(figsize=(12, 6))
                for name in category_df['name'].unique():
                    name_df = category_df[category_df['name'] == name]
                    plt.plot(name_df['timestamp'], name_df['value'], label=name, marker='o')
                
                plt.title(f"{category} Metrics Over Time")
                plt.xlabel("Timestamp")
                plt.ylabel("Value")
                plt.legend()
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                # Save plot
                plot_file = self.data_dir / f"plot_{category}_{period}.png"
                plt.savefig(plot_file)
                plt.close()
            
        except Exception as e:
            self.logger.error(f"Failed to create visualizations: {str(e)}")
    
    def _save_report(self, report: AnalyticsReport):
        """Save analytics report"""
        try:
            report_file = self.data_dir / f"report_{report.period}_{datetime.now().strftime('%Y%m%d')}.json"
            
            with open(report_file, 'w') as f:
                json.dump({
                    'metrics': [metric.__dict__ for metric in report.metrics],
                    'insights': report.insights,
                    'period': report.period,
                    'generated_at': report.generated_at
                }, f, indent=4)
                
        except Exception as e:
            self.logger.error(f"Failed to save report: {str(e)}")
    
    def get_metric_history(self, metric_name: str, period: str = 'weekly') -> List[Tuple[str, float]]:
        """Get historical values for a metric"""
        try:
            end_date = datetime.now()
            if period == 'daily':
                start_date = end_date - timedelta(days=1)
            elif period == 'weekly':
                start_date = end_date - timedelta(weeks=1)
            elif period == 'monthly':
                start_date = end_date - timedelta(days=30)
            else:
                raise ValueError(f"Invalid period: {period}")
            
            query = text("""
                SELECT timestamp, value
                FROM analytics_metrics
                WHERE name = :metric_name
                AND timestamp BETWEEN :start_date AND :end_date
                ORDER BY timestamp ASC
            """)
            
            with self.db_engine.connect() as conn:
                result = conn.execute(
                    query,
                    {
                        'metric_name': metric_name,
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat()
                    }
                )
                
                return [(row.timestamp, row.value) for row in result]
                
        except Exception as e:
            self.logger.error(f"Failed to get metric history: {str(e)}")
            return []
    
    def cleanup(self):
        """Cleanup analytics system resources"""
        try:
            if self.db_engine:
                self.db_engine.dispose()
            
            self.initialized = False
            self.logger.info("Analytics system resources cleaned up")
            
        except Exception as e:
            self.logger.error(f"Analytics system cleanup failed: {str(e)}")
