import React, { useState } from 'react';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { fab } from '@fortawesome/free-brands-svg-icons';
import {
  fas,
  faCaretDown,
  faCaretUp,
  faCheckCircle,
  faTimesCircle
} from '@fortawesome/free-solid-svg-icons';
import { IconName, IconPrefix } from '@fortawesome/fontawesome-svg-core';
import StyledParameterComponent from './WorkflowParameter';
import { ParameterSection } from './types';
import styled from 'styled-components';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IParameterSectionComponent extends ParameterSection {
  errors: { [key: string]: string[] };
  onChange: CallableFunction;
  className?: string;
  initOpen: boolean;
}

const ParameterSectionComponent = ({
  title,
  fa_icon,
  properties,
  errors,
  initOpen,
  onChange,
  className
}: IParameterSectionComponent): JSX.Element => {
  // ------------------------------------
  // Set up state
  // ------------------------------------
  const [isOpen, setIsOpen] = useState(initOpen);
  const isValid = Object.keys(errors).length === 0 ? true : false;

  // ------------------------------------
  // Handle fa_icon
  // ------------------------------------
  library.add(fas, fab);
  const iconName = fa_icon?.split(' ')[1];
  const iconPrefix = fa_icon?.split(' ')[0];
  const iconNameStripped = iconName?.startsWith('fa-')
    ? iconName.split('fa-')[1]
    : iconName;

  return (
    <div className={`parameter-section ${className}`}>
      <div className={`parameter-section-container ${isValid ? 'valid' : ''}`}>
        <button
          className="parameter-section-toggle"
          onClick={() => setIsOpen(!isOpen)}
        >
          <h3>
            {typeof fa_icon === 'string' ? (
              <FontAwesomeIcon
                icon={[iconPrefix as IconPrefix, iconNameStripped as IconName]}
              />
            ) : (
              ''
            )}
            {title}
          </h3>
          <div className="parameter-section-toggle-controls">
            <FontAwesomeIcon icon={isOpen ? faCaretUp : faCaretDown} />
            {isValid ? (
              <div className="parameter-section-toggle-errors valid">
                <FontAwesomeIcon icon={faCheckCircle} />
              </div>
            ) : (
              <div className="parameter-section-toggle-errors invalid">
                <FontAwesomeIcon icon={faTimesCircle} />
              </div>
            )}
          </div>
        </button>
        <ul className={`parameter-section-items ${isOpen ? 'open' : 'closed'}`}>
          {Object.entries(properties)
            .sort(([, a_prop], [, b_prop]) => a_prop.order - b_prop.order)
            .map(([key, value]) => (
              <li>
                <StyledParameterComponent
                  id={key}
                  schema={value}
                  error={errors[key] || []}
                  onChange={onChange}
                />
              </li>
            ))}
        </ul>
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledParameterSectionComponent = styled(ParameterSectionComponent)`
  && {
    margin: 25px 0;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    background-color: white;
    border-radius: 4px;
  }

  .parameter-section-toggle {
    box-sizing: border-box;
    width: 100%;
    display: flex;
    padding: 25px;
    justify-content: space-between;
    align-items: center;
    border: none;
    outline: none;
    background-color: transparent;
    cursor: pointer;
  }

  .parameter-section-toggle:hover {
    background-color: #f3f3f3;
  }

  .parameter-section-toggle h3 svg {
    margin-right: 15px;
  }

  .parameter-section-toggle-controls {
    display: flex;
  }

  .parameter-section-toggle-controls svg {
    width: 18px;
    height: 18px;
  }

  .parameter-section-toggle-errors {
    display: flex;
    align-items: center;
  }

  .parameter-section-toggle-errors svg {
    margin-left: 5px;
  }

  .parameter-section-toggle-errors.valid svg {
    color: #1d9655;
  }

  .parameter-section-toggle-errors.invalid svg {
    // color: #e34040;
    color: #e11515;
  }

  .parameter-section-toggle-errors.invalid p {
    font-weight: bold;
    color: #e34040;
  }

  .parameter-section-items {
    display: block;
    transition: 0.2s ease-in-out all;
  }

  .parameter-section-items.closed {
    display: none;
  }

  .parameter-section-items.open {
    display: block;
    background-color: #fff;
  }

  .parameter-section-items > li {
    padding: 25px 0;
    width: calc(100% - 50px);
    margin: 0 auto;
    box-sizing: border-box;
    background-color: #fff;
    border-top: 1px solid #f2f2f2;
    color: #212529;
  }
`;

export default StyledParameterSectionComponent;
