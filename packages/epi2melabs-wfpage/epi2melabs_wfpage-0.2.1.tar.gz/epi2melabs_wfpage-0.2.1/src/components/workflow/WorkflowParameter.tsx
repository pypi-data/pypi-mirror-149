import React from 'react';
import { Parameter } from './types';
import { getInputComponent } from './inputs';
import styled from 'styled-components';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IParameterComponent {
  id: string;
  schema: Parameter;
  error: string[];
  onChange: CallableFunction;
  className?: string;
}

const ParameterComponent = ({
  id,
  schema,
  error,
  onChange,
  className
}: IParameterComponent): JSX.Element => (
  <div className={`parameter ${className}`}>
    {getInputComponent(id, schema, error, onChange)}
  </div>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledParameterComponent = styled(ParameterComponent)`
  padding: 25px 15px;
`;

export default StyledParameterComponent;
