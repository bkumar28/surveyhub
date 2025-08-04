import React, { useEffect, useState } from 'react';
import { fetchSurveys } from '../../services/api';
import Loader from '../common/Loader';
import Notification from '../common/Notification';

const SurveyList = () => {
  const [surveys, setSurveys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getSurveys = async () => {
      try {
        const data = await fetchSurveys();
        setSurveys(data);
      } catch (err) {
        setError('Failed to fetch surveys');
      } finally {
        setLoading(false);
      }
    };

    getSurveys();
  }, []);

  if (loading) {
    return <Loader />;
  }

  if (error) {
    return <Notification message={error} />;
  }

  return (
    <div className="survey-list">
      <h2>Available Surveys</h2>
      <ul className="list-group">
        {surveys.map(survey => (
          <li key={survey.id} className="list-group-item">
            <a href={`/surveys/${survey.id}`} className="nav-link">
              {survey.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SurveyList;
