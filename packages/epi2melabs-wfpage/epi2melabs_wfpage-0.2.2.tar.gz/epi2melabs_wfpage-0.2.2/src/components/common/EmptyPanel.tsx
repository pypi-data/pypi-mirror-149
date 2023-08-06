import React from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { IconDefinition } from '@fortawesome/free-solid-svg-icons';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IEmptyPanel {
  className?: string;
  body: string;
  icon: IconDefinition;
}

const EmptyPanel = ({ className, body, icon }: IEmptyPanel): JSX.Element => (
  <div className={className}>
    <div className="empty">
      <FontAwesomeIcon icon={icon} />
      <h4>{body}</h4>
    </div>
  </div>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledEmptyPanel = styled(EmptyPanel)`
  && {
    margin: 0 auto;
    box-sizing: border-box;
  }

  .empty {
    width: 100%;
    height: 250px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    background-color: #ffffff;
  }

  .empty svg {
    padding-bottom: 15px;
    color: lightgray;
  }
`;

export default StyledEmptyPanel;
