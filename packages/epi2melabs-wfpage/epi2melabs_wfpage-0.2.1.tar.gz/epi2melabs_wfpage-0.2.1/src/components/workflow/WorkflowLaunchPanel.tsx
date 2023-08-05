import React from 'react';
import { GenericStringObject, GenericObject } from '../../types';
import StyledWorkflowParameterSection from './WorkflowParameterSection';
import { ParameterSection, Parameter } from './types';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faCheckCircle,
  faTimesCircle
} from '@fortawesome/free-solid-svg-icons';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IWorkflowLaunchPanel {
  className?: string;
  parameterSections: ParameterSection[];
  parameterErrors: GenericObject;
  parametersValid: boolean;
  instanceName: string | null;
  instanceNameError: string | null;
  instanceCreateError: string | null;
  onChangeInstanceName: (name: string) => void;
  onChangeParameter: (id: string, format: string, value: any) => unknown;
  onClickLaunch: () => void;
}

const WorkflowLaunchPanel = ({
  className,
  parameterSections,
  parameterErrors,
  parametersValid,
  onChangeParameter,
  instanceName,
  instanceNameError,
  instanceCreateError,
  onChangeInstanceName,
  onClickLaunch
}: IWorkflowLaunchPanel): JSX.Element => {
  // ------------------------------------
  // Handle parameter validation
  // ------------------------------------
  const filterErrorsByParameters = (
    parameters: { [key: string]: Parameter },
    errors: GenericStringObject
  ) =>
    Object.keys(parameters).reduce(
      (obj, key) =>
        Object.prototype.hasOwnProperty.call(errors, key)
          ? {
              ...obj,
              [key]: errors[key]
            }
          : obj,
      {}
    );

  return (
    <div className={`launch-panel ${className}`}>
      {/* Instance name */}
      <div className={`instance-name ${instanceName ? '' : 'invalid'}`}>
        <input
          id="worflow-name-input"
          type="text"
          placeholder={'Name your experiment...'}
          onChange={e => onChangeInstanceName(e.target.value)}
          maxLength={50}
        />
        <div
          className={`instance-name-input-errors ${
            instanceNameError || !instanceName ? 'invalid' : ''
          }`}
        >
          {instanceNameError || !instanceName ? (
            <FontAwesomeIcon icon={faTimesCircle} />
          ) : (
            <FontAwesomeIcon icon={faCheckCircle} />
          )}
        </div>
      </div>

      {/* Workflow params */}
      <div className="parameter-sections">
        <ul>
          {parameterSections.map((Section, idx) => (
            <li>
              <StyledWorkflowParameterSection
                title={Section.title}
                description={Section.description}
                fa_icon={Section.fa_icon}
                initOpen={idx ? false : true}
                properties={Section.properties}
                errors={filterErrorsByParameters(
                  Section.properties,
                  parameterErrors
                )}
                onChange={onChangeParameter}
              />
            </li>
          ))}
        </ul>
      </div>

      {/* Workflow launch */}
      <div
        className={`launch-control ${
          parametersValid && instanceName ? 'active' : 'inactive'
        }`}
      >
        <button onClick={() => onClickLaunch()}>Launch Workflow</button>
        {instanceCreateError ? (
          <div className="error">
            <p>Error: {instanceCreateError}</p>
          </div>
        ) : (
          ''
        )}
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledWorkflowLaunchPanel = styled(WorkflowLaunchPanel)`
  //
  // Instance naming
  //
  .instance-name {
    position: relative;
  }

  .instance-name input {
    box-sizing: border-box;
    width: 100%;
    margin: 0;
    padding: 25px;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    background-color: white;
    border: none;
    border-radius: 4px;
    outline: none;
    transition: 0.2s ease-in-out all;
  }

  .instance-name.invalid input {
    color: #e34040;
  }

  .instance-name-input-errors {
    position: absolute;
    top: 25px;
    right: 25px;
  }

  .instance-name-input-errors svg {
    width: 18px;
    height: 18px;
    color: #1d9655;
  }

  .instance-name-input-errors.invalid svg {
    color: #e34040;
  }

  //
  // Launch control
  //
  .launch-control {
    margin: 15px 0 0 0;
  }

  .launch-control button {
    box-sizing: border-box;
    width: 100%;
    padding: 25px 25px;
    border: 0;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    cursor: pointer;
  }

  .launch-control.active button {
    border: 1px solid #1d9655;
    background-color: #1d9655;
    color: white;
  }
  .launch-control.active button:hover {
    cursor: pointer;
    background-color: white;
    color: #1d9655;
  }
  .launch-control.error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`;

export default StyledWorkflowLaunchPanel;
