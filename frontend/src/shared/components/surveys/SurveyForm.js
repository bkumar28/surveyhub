import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import '../../assets/css/app.css';

const SurveyForm = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const history = useHistory();

  const handleSubmit = (e) => {
    e.preventDefault();
    // Logic to handle form submission, e.g., API call to save the survey
    console.log('Survey submitted:', { title, description });
    history.push('/surveys'); // Redirect to surveys list after submission
  };

  return (
    <div className="survey-form container">
      <h2>Create a New Survey</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="title" className="form-label">Survey Title</label>
          <input
            type="text"
            className="form-control"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="description" className="form-label">Description</label>
          <textarea
            className="form-control"
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          ></textarea>
        </div>
        <button type="submit" className="btn btn-primary">Submit</button>
      </form>
    </div>
  );
};

export default SurveyForm;
