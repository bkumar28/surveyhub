import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../services/api';
import Loader from '../common/Loader';
import Notification from '../common/Notification';

const SurveyDetail = () => {
  const { id } = useParams();
  const [survey, setSurvey] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSurvey = async () => {
      try {
        const response = await api.get(`/surveys/${id}`);
        setSurvey(response.data);
      } catch (err) {
        setError('Failed to fetch survey details.');
      } finally {
        setLoading(false);
      }
    };

    fetchSurvey();
  }, [id]);

  if (loading) {
    return <Loader />;
  }

  if (error) {
    return <Notification message={error} />;
  }

  return (
    <div className="survey-detail container">
      <h1>{survey.title}</h1>
      <p>{survey.description}</p>
      <h3>Questions:</h3>
      <ul>
        {survey.questions.map((question, index) => (
          <li key={index}>{question}</li>
        ))}
      </ul>
    </div>
  );
};

export default SurveyDetail;
