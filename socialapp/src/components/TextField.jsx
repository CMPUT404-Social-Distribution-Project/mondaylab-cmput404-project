import React from 'react'
import { ErrorMessage, useField } from 'formik';

export default function TextField({label, ...props}) {
    const [field, meta] = useField(props);
    return (
        <div className='mb-2 mt-4'>
            <label htmlFor={field.name}>{label}</label>
            <input 
                className={`form-control shadow-none ${meta.touched && meta.error && 'is-invalid'}`}
                {...field} {...props}
                autoComplete="off"
            />
            <ErrorMessage component="div" name={field.name} className='err-validate-mes'/>
        </div>
    )
}

