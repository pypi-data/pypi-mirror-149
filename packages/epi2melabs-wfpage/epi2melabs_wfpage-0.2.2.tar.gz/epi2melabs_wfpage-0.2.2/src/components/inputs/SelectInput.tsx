import React from 'react';
import styled from 'styled-components';

// -----------------------------------------------------------------------------
// Type definitions
// -----------------------------------------------------------------------------
export const SELECT_INPUT = 'select';

interface ISelectChoice {
  value: string;
  label: string;
}

export interface ISelectProps {
  id: string;
  label: string;
  format: string;
  description: string;
  defaultValue?: string;
  choices: ISelectChoice[];
}

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface ISelectInput extends ISelectProps {
  error: string[];
  onChange: CallableFunction;
  className?: string;
}

const SelectInput = ({
  id,
  label,
  format,
  description,
  defaultValue,
  choices,
  error,
  onChange,
  className
}: ISelectInput): JSX.Element => (
  <div className={`SelectInput ${className}`}>
    <h4>{label}</h4>
    <p>{description}</p>
    <label htmlFor={id}>
      <select
        id={id}
        onChange={(e: any) => onChange(id, format, e.target.value)}
      >
        {defaultValue ? (
          ''
        ) : (
          <option
            className="placeholder"
            selected
            disabled
            hidden
            value="Select an option"
          >
            Select an option
          </option>
        )}
        {choices.map(Choice => (
          <option
            key={Choice.label}
            selected={!!(Choice.value === defaultValue)}
            value={Choice.value}
          >
            {Choice.label}
          </option>
        ))}
      </select>
    </label>
    {error.length ? (
      <div className="error">
        {error.map(Error => (
          <p>Error: {Error}</p>
        ))}
      </div>
    ) : (
      ''
    )}
  </div>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledSelectInput = styled(SelectInput)`
  h4 {
    padding: 0 0 5px 0;
  }

  p {
    padding: 0 0 10px 0;
  }

  label {
    display: flex;
  }

  select {
    margin: 0;
    min-width: 50%;
    padding: 15px 25px;

    font-size: 14px;
    line-height: 1em;

    color: #212529;
    background-color: #f8f9fa;
    border: 1px solid rgba(0, 0, 0, 0.125);
    border-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  select:hover {
    border-color: #005c75;
    box-shadow: 0 0 0 0.25rem rgb(13 110 253 / 25%);
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`;

export default StyledSelectInput;
