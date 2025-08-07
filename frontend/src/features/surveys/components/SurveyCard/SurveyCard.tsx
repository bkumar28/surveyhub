import React from 'react';
import { Card } from '../../../../shared/components/UI/Card';
import { Button } from '../../../../shared/components/UI/Button';
import styles from './SurveyCard.module.scss';

interface Survey {
  id: string;
  title: string;
  description: string;
  status: 'draft' | 'published' | 'closed';
  createdAt: string;
  responseCount: number;
}

interface SurveyCardProps {
  survey: Survey;
  onEdit?: (survey: Survey) => void;
  onDelete?: (surveyId: string) => void;
  onView?: (survey: Survey) => void;
}

export const SurveyCard: React.FC<SurveyCardProps> = ({
  survey,
  onEdit,
  onDelete,
  onView,
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published':
        return 'var(--color-success)';
      case 'draft':
        return 'var(--color-warning)';
      case 'closed':
        return 'var(--color-gray-500)';
      default:
        return 'var(--color-gray-500)';
    }
  };

  return (
    <Card className={styles.card}>
      <div className={styles.header}>
        <div className={styles.info}>
          <h3 className={styles.title}>{survey.title}</h3>
          <p className={styles.description}>{survey.description}</p>
        </div>
        <span
          className={styles.status}
          style={{ color: getStatusColor(survey.status) }}
        >
          {survey.status}
        </span>
      </div>

      <div className={styles.meta}>
        <span className={styles.responses}>
          {survey.responseCount} responses
        </span>
        <span className={styles.date}>
          Created {new Date(survey.createdAt).toLocaleDateString()}
        </span>
      </div>

      <div className={styles.actions}>
        {onView && (
          <Button variant="outline" size="sm" onClick={() => onView(survey)}>
            View
          </Button>
        )}
        {onEdit && (
          <Button variant="secondary" size="sm" onClick={() => onEdit(survey)}>
            Edit
          </Button>
        )}
        {onDelete && (
          <Button variant="danger" size="sm" onClick={() => onDelete(survey.id)}>
            Delete
          </Button>
        )}
      </div>
    </Card>
  );
};
