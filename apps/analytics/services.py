import pandas as pd
import numpy as np
from django.db.models import Count, Avg, Q, F
from django.utils import timezone
from datetime import timedelta
import json
from collections import Counter
import re

from apps.surveys.models import Survey, SurveyResponse, Answer, Question
from .models import SurveyAnalytics, QuestionAnalytics

class AnalyticsService:
    def __init__(self):
        self.sentiment_keywords = {
            'positive': ['good', 'great', 'excellent', 'amazing', 'love', 'perfect', 'wonderful'],
            'negative': ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disappointing']
        }
    
    def update_survey_analytics(self, survey):
        """Update analytics for a survey"""
        analytics, created = SurveyAnalytics.objects.get_or_create(survey=survey)
        
        # Get all responses
        responses = survey.responses.all()
        completed_responses = responses.filter(is_complete=True)
        
        # Basic metrics
        analytics.total_starts = responses.count()
        analytics.total_completions = completed_responses.count()
        analytics.completion_rate = (
            (analytics.total_completions / analytics.total_starts * 100) 
            if analytics.total_starts > 0 else 0
        )
        
        # Time metrics
        completed_with_time = completed_responses.exclude(time_taken__isnull=True)
        if completed_with_time.exists():
            times = [r.time_taken.total_seconds() for r in completed_with_time]
            analytics.average_completion_time = timedelta(seconds=np.mean(times))
            analytics.median_completion_time = timedelta(seconds=np.median(times))
        
        # Device analytics
        analytics.mobile_responses = responses.filter(
            user_agent__icontains='Mobile'
        ).count()
        analytics.desktop_responses = responses.exclude(
            Q(user_agent__icontains='Mobile') | Q(user_agent__icontains='Tablet')
        ).count()
        analytics.tablet_responses = responses.filter(
            user_agent__icontains='Tablet'
        ).count()
        
        # Geographic analytics
        countries = Counter(responses.exclude(country='').values_list('country', flat=True))
        cities = Counter(responses.exclude(city='').values_list('city', flat=True))
        analytics.top_countries = dict(countries.most_common(10))
        analytics.top_cities = dict(cities.most_common(10))
        
        # Traffic sources (simplified)
        referrers = Counter(responses.exclude(referrer='').values_list('referrer', flat=True))
        analytics.traffic_sources = dict(referrers.most_common(10))
        
        analytics.save()
        
        # Update question analytics
        for question in survey.questions.all():
            self.update_question_analytics(question)
    
    def update_question_analytics(self, question):
        """Update analytics for a specific question"""
        analytics, created = QuestionAnalytics.objects.get_or_create(question=question)
        
        answers = Answer.objects.filter(question=question)
        analytics.total_answers = answers.count()
        
        # Count skipped questions (responses without answers for this question)
        total_responses = question.survey.responses.filter(is_complete=True).count()
        analytics.skip_count = total_responses - analytics.total_answers
        
        if question.field_type in ['MC', 'CB', 'RD']:  # Multiple choice questions
            self._analyze_choice_question(question, analytics, answers)
        elif question.field_type in ['N', 'RT', 'SL']:  # Numeric questions
            self._analyze_numeric_question(question, analytics, answers)
        elif question.field_type == 'T':  # Text questions
            self._analyze_text_question(question, analytics, answers)
        
        analytics.save()
    
    def _analyze_choice_question(self, question, analytics, answers):
        """Analyze multiple choice questions"""
        choice_counts = {}
        
        for answer in answers:
            if answer.json_answer:
                # Handle multiple selections (checkbox)
                if isinstance(answer.json_answer, list):
                    for choice in answer.json_answer:
                        choice_counts[choice] = choice_counts.get(choice, 0) + 1
                else:
                    choice = answer.json_answer
                    choice_counts[choice] = choice_counts.get(choice, 0) + 1
            elif answer.text_answer:
                choice = answer.text_answer
                choice_counts[choice] = choice_counts.get(choice, 0) + 1
        
        analytics.choice_distribution = choice_counts
    
    def _analyze_numeric_question(self, question, analytics, answers):
        """Analyze numeric questions"""
        values = []
        for answer in answers:
            if answer.number_answer is not None:
                values.append(answer.number_answer)
        
        if values:
            analytics.average_value = np.mean(values)
            analytics.median_value = np.median(values)
            analytics.min_value = min(values)
            analytics.max_value = max(values)
    
    def _analyze_text_question(self, question, analytics, answers):
        """Analyze text questions"""
        texts = [answer.text_answer for answer in answers if answer.text_answer]
        
        if texts:
            # Word frequency analysis
            all_text = ' '.join(texts).lower()
            words = re.findall(r'\b\w+\b', all_text)
            word_freq = Counter(words)
            
            # Remove common stop words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            filtered_words = {k: v for k, v in word_freq.items() if k not in stop_words and len(k) > 2}
            
            analytics.word_cloud_data = dict(Counter(filtered_words).most_common(50))
            
            # Simple sentiment analysis
            sentiment_score = self._calculate_sentiment(texts)
            analytics.sentiment_score = sentiment_score
    
    def _calculate_sentiment(self, texts):
        """Simple sentiment analysis"""
        total_score = 0
        total_words = 0
        
        for text in texts:
            words = text.lower().split()
            text_score = 0
            
            for word in words:
                if word in self.sentiment_keywords['positive']:
                    text_score += 1
                elif word in self.sentiment_keywords['negative']:
                    text_score -= 1
            
            total_score += text_score
            total_words += len(words)
        
        return total_score / total_words if total_words > 0 else 0
    
    def generate_comprehensive_report(self, survey):
        """Generate a comprehensive analytics report"""
        # Update analytics first
        self.update_survey_analytics(survey)
        
        analytics = survey.analytics
        responses = survey.responses.filter(is_complete=True)
        
        report = {
            'survey_info': {
                'id': survey.id,
                'title': survey.title,
                'description': survey.description,
                'created_at': survey.created_at,
                'status': survey.status,
            },
            'response_metrics': {
                'total_views': analytics.total_views,
                'total_starts': analytics.total_starts,
                'total_completions': analytics.total_completions,
                'completion_rate': analytics.completion_rate,
                'bounce_rate': analytics.bounce_rate,
            },
            'time_metrics': {
                'average_completion_time': str(analytics.average_completion_time) if analytics.average_completion_time else None,
                'median_completion_time': str(analytics.median_completion_time) if analytics.median_completion_time else None,
            },
            'device_breakdown': {
                'mobile': analytics.mobile_responses,
                'desktop': analytics.desktop_responses,
                'tablet': analytics.tablet_responses,
            },
            'geographic_data': {
                'top_countries': analytics.top_countries,
                'top_cities': analytics.top_cities,
            },
            'traffic_sources': analytics.traffic_sources,
            'question_analytics': [],
            'trends': self._generate_trends(survey),
            'insights': self._generate_insights(survey),
            'generated_at': timezone.now().isoformat(),
        }
        
        # Add question-specific analytics
        for question in survey.questions.all():
            if hasattr(question, 'analytics'):
                q_analytics = question.analytics
                question_data = {
                    'question_id': question.id,
                    'question_title': question.title,
                    'question_type': question.field_type,
                    'total_answers': q_analytics.total_answers,
                    'skip_count': q_analytics.skip_count,
                    'skip_rate': (q_analytics.skip_count / analytics.total_starts * 100) if analytics.total_starts > 0 else 0,
                }
                
                if question.field_type in ['MC', 'CB', 'RD']:
                    question_data['choice_distribution'] = q_analytics.choice_distribution
                elif question.field_type in ['N', 'RT', 'SL']:
                    question_data.update({
                        'average_value': q_analytics.average_value,
                        'median_value': q_analytics.median_value,
                        'min_value': q_analytics.min_value,
                        'max_value': q_analytics.max_value,
                    })
                elif question.field_type == 'T':
                    question_data.update({
                        'word_cloud_data': q_analytics.word_cloud_data,
                        'sentiment_score': q_analytics.sentiment_score,
                    })
                
                report['question_analytics'].append(question_data)
        
        return report
    
    def _generate_trends(self, survey):
        """Generate trend data for the survey"""
        responses = survey.responses.filter(is_complete=True).order_by('completed_at')
        
        if not responses.exists():
            return {}
        
        # Daily response trend
        daily_responses = {}
        for response in responses:
            date_key = response.completed_at.date().isoformat()
            daily_responses[date_key] = daily_responses.get(date_key, 0) + 1
        
        return {
            'daily_responses': daily_responses,
            'peak_response_day': max(daily_responses.items(), key=lambda x: x[1]) if daily_responses else None,
        }
    
    def _generate_insights(self, survey):
        """Generate AI-like insights"""
        insights = []
        analytics = survey.analytics
        
        # Completion rate insights
        if analytics.completion_rate > 80:
            insights.append({
                'type': 'positive',
                'title': 'High Completion Rate',
                'description': f'Your survey has an excellent completion rate of {analytics.completion_rate:.1f}%'
            })
        elif analytics.completion_rate < 30:
            insights.append({
                'type': 'warning',
                'title': 'Low Completion Rate',
                'description': f'Your survey completion rate is {analytics.completion_rate:.1f}%. Consider shortening the survey or improving question clarity.'
            })
        
        # Device insights
        total_responses = analytics.mobile_responses + analytics.desktop_responses + analytics.