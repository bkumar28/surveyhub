import React, { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../../../../app/store';
import { fetchSurveys } from '../../surveysSlice';
import { SurveyCard } from '../../components/SurveyCard';
import { Button } from '../../../../shared/components/UI/Button';
import styles from './SurveysPage.module.scss';

export const SurveysPage: React.FC = () => {
  const dispatch = useAppDispatch();
  const { surveys, loading, error } = useAppSelector((state) => state.surveys);

  useEffect(() => {
    dispatch(fetchSurveys());
  }, [dispatch]);

  const handleCreateSurvey = () => {
    // Navigate to create survey page
    console.log('Create new survey');
  };

  const handleEditSurvey = (survey: any) => {
    console.log('Edit survey:', survey);
  };

  const handleDeleteSurvey = (surveyId: string) => {
    console.log('Delete survey:', surveyId);
  };

  const handleViewSurvey = (survey: any) => {
    console.log('View survey:', survey);
  };

  if (loading) {
    return <div className={styles.loading}>Loading surveys...</div>;
  }

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div className={styles.headerContent}>
          <h1>Surveys</h1>
          <p>Create, manage, and analyze your surveys</p>
        </div>
        <Button onClick={handleCreateSurvey}>
          Create Survey
        </Button>
      </div>

      {error && (
        <div className={styles.error}>
          Error loading surveys: {error}
        </div>
      )}

      {surveys.length === 0 ? (
        <div className={styles.empty}>
          <div className={styles.emptyContent}>
            <h2>No surveys yet</h2>
            <p>Create your first survey to get started</p>
            <Button onClick={handleCreateSurvey}>
              Create Your First Survey
            </Button>
          </div>
        </div>
      ) : (
        <div className={styles.grid}>
          {surveys.map((survey) => (
            <SurveyCard
              key={survey.id}
              survey={survey}
              onEdit={handleEditSurvey}
              onDelete={handleDeleteSurvey}
              onView={handleViewSurvey}
            />
          ))}
        </div>
      )}
    </div>
  );
};
