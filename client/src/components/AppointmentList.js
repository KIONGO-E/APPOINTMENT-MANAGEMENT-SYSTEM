import React, { useState, useEffect } from 'react';

const AppointmentsList = () => {
  const [appointments, setAppointments] = useState([]);
  const [filter, setFilter] = useState('');
  const [sort, setSort] = useState('date');

  useEffect(() => {
    fetch('/api/appointments')
      .then(response => response.json())
      .then(data => setAppointments(data));
  }, []);

  const filteredAppointments = appointments.filter(appointment =>
    appointment.title.toLowerCase().includes(filter.toLowerCase())
  );

  const sortedAppointments = filteredAppointments.sort((a, b) => {
    if (sort === 'date') {
      return new Date(a.date) - new Date(b.date);
    } else if (sort === 'title') {
      return a.title.localeCompare(b.title);
    }
    return 0;
  });

  return (
    <div>
      <h2>Appointments</h2>
      <div>
        <label>Filter by Title:</label>
        <input
          type="text"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
      </div>
      <div>
        <label>Sort by:</label>
        <select value={sort} onChange={(e) => setSort(e.target.value)}>
          <option value="date">Date</option>
          <option value="title">Title</option>
        </select>
      </div>
      <ul>
        {sortedAppointments.map(appointment => (
          <li key={appointment.id}>
            <strong>{appointment.title}</strong>
            <p>{appointment.date} at {appointment.time}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AppointmentsList;
