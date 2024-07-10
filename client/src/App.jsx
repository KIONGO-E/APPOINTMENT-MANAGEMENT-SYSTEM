import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import NavBar from './components/NavBar';
import SignupForm from './components/SignupForm';
import LoginForm from './components/LoginForm';
import HomePage from './components/HomePage';
import AppointmentsPage from './components/AppointmentsPage';
import AppointmentForm from './components/AppointmentForm';
import AppointmentsList from './components/AppointmentsList';
import reactLogo from './assets/react.svg';
import viteLogo from './assets/vite.svg';
import './App.css';

const App = () => {
  const handleAppointmentSubmit = (values) => {
    const url = values.id ? `/api/appointments/${values.id}` : '/api/appointments';
    const method = values.id ? 'PUT' : 'POST';

    fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(values),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  return (
    <Router>
      <NavBar />
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <Switch>
          <Route path="/" exact component={HomePage} />
          <Route path="/signup" component={SignupForm} />
          <Route path="/login" component={LoginForm} />
          <Route path="/appointments" exact component={AppointmentsList} />
          <Route path="/appointments/new" render={() => (
            <AppointmentForm initialValues={{ title: '', date: '', time: '' }} onSubmit={handleAppointmentSubmit} />
          )} />
          <Route path="/appointments/:id/edit" render={({ match }) => {
            const appointmentId = match.params.id;
            const initialValues = { title: '', date: '', time: '', id: appointmentId };
            return <AppointmentForm initialValues={initialValues} onSubmit={handleAppointmentSubmit} />;
          }} />
        </Switch>
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </Router>
  );
};

export default App;
