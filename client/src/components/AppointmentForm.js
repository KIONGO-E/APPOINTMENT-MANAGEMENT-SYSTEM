import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const AppointmentForm = ({ initialValues, onSubmit }) => {
  const validationSchema = Yup.object().shape({
    title: Yup.string().required('Title is required'),
    date: Yup.date().required('Date is required'),
    time: Yup.string().required('Time is required'),
  });

  return (
    <div>
      <h2>{initialValues.id ? 'Edit Appointment' : 'Create Appointment'}</h2>
      <Formik
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={onSubmit}
      >
        <Form>
          <div>
            <label>Title</label>
            <Field name="title" type="text" />
            <ErrorMessage name="title" component="div" />
          </div>
          <div>
            <label>Date</label>
            <Field name="date" type="date" />
            <ErrorMessage name="date" component="div" />
          </div>
          <div>
            <label>Time</label>
            <Field name="time" type="time" />
            <ErrorMessage name="time" component="div" />
          </div>
          <button type="submit">{initialValues.id ? 'Update' : 'Create'}</button>
        </Form>
      </Formik>
    </div>
  );
};

export default AppointmentForm;
