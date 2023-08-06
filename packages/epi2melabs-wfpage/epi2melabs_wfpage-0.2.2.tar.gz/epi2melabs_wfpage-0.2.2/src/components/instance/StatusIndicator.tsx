import React from 'react';
import styled from 'styled-components';
import { GenericObject } from '../../types';

const UNKNOWN = 'UNKNOWN';
const LAUNCHED = 'LAUNCHED';
const ENCOUNTERED_ERROR = 'ENCOUNTERED_ERROR';
const COMPLETED_SUCCESSFULLY = 'COMPLETED_SUCCESSFULLY';
const TERMINATED = 'TERMINATED';

export const finished = [COMPLETED_SUCCESSFULLY, TERMINATED, ENCOUNTERED_ERROR];

const statuses: GenericObject = {
  [UNKNOWN]: {
    name: 'UNKNOWN',
    className: 'grey'
  },
  [LAUNCHED]: {
    name: 'LAUNCHED',
    className: 'blue'
  },
  [ENCOUNTERED_ERROR]: {
    name: 'ENCOUNTERED_ERROR',
    className: 'orange'
  },
  [COMPLETED_SUCCESSFULLY]: {
    name: 'COMPLETED_SUCCESSFULLY',
    className: 'green'
  },
  [TERMINATED]: {
    name: 'TERMINATED',
    className: 'black'
  }
};

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IStatusIndicator {
  status: string;
  className?: string;
}

const StatusIndicator = ({
  status,
  className
}: IStatusIndicator): JSX.Element => {
  return (
    <div className={`status-indicator ${className}`}>
      <div className={statuses[status].className}></div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledStatusIndicator = styled(StatusIndicator)`
  > div {
    width: 16px;
    height: 16px;
    padding: 0;
    border-radius: 100%;
    line-height: 18px;
    text-align: center;
    font-size: 10px;
    color: white;
  }

  .blue {
    cursor: pointer;
    background-color: #005c75;
    box-shadow: 0 0 0 rgba(204, 169, 44, 0.4);
    animation: pulse-blue 2s infinite;
  }

  @keyframes pulse-blue {
    0% {
      -moz-box-shadow: 0 0 0 0 rgba(44, 119, 204, 0.4);
      box-shadow: 0 0 0 0 rgba(44, 119, 204, 0.4);
    }
    70% {
      -moz-box-shadow: 0 0 0 10px rgba(44, 119, 204, 0);
      box-shadow: 0 0 0 10px rgba(44, 119, 204, 0);
    }
    100% {
      -moz-box-shadow: 0 0 0 0 rgba(44, 119, 204, 0);
      box-shadow: 0 0 0 0 rgba(44, 119, 204, 0);
    }
  }

  .orange {
    cursor: pointer;
    background-color: #e34040;
    box-shadow: 0 0 0 rgba(23, 187, 117, 0.4);
    animation: pulse-orange 2s infinite;
  }

  @keyframes pulse-orange {
    0% {
      -moz-box-shadow: 0 0 0 0 rgba(255, 140, 0, 0.4);
      box-shadow: 0 0 0 0 rgba(255, 140, 0, 0.4);
    }
    70% {
      -moz-box-shadow: 0 0 0 10px rgba(255, 140, 0, 0);
      box-shadow: 0 0 0 10px rgba(255, 140, 0, 0);
    }
    100% {
      -moz-box-shadow: 0 0 0 0 rgba(255, 140, 0, 0);
      box-shadow: 0 0 0 0 rgba(255, 140, 0, 0);
    }
  }

  .green {
    cursor: pointer;
    background-color: #17bb75;
    box-shadow: 0 0 0 rgba(23, 187, 117, 0.4);
    animation: pulse-green 2s infinite;
  }

  @keyframes pulse-green {
    0% {
      -moz-box-shadow: 0 0 0 0 rgba(23, 187, 117, 0.4);
      box-shadow: 0 0 0 0 rgba(23, 187, 117, 0.4);
    }
    70% {
      -moz-box-shadow: 0 0 0 10px rgba(23, 187, 117, 0);
      box-shadow: 0 0 0 10px rgba(23, 187, 117, 0);
    }
    100% {
      -moz-box-shadow: 0 0 0 0 rgba(23, 187, 117, 0);
      box-shadow: 0 0 0 0 rgba(23, 187, 117, 0);
    }
  }

  .grey {
    background-color: #707070;
  }

  .black {
    background-color: black;
  }
`;

export default StyledStatusIndicator;
