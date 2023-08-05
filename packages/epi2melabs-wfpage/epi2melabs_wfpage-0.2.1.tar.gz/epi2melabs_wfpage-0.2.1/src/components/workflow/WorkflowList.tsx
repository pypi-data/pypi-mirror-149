import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { requestAPI } from '../../handler';
import { Workflow } from './types';
import StyledEmptyPanel from '../common/EmptyPanel';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDna, faFolderOpen } from '@fortawesome/free-solid-svg-icons';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IWorkflowsList {
  className?: string;
}

const WorkflowsList = ({ className }: IWorkflowsList): JSX.Element => {
  // ------------------------------------
  // Set up state
  // ------------------------------------
  const [workflows, setWorkflows] = useState<Workflow[]>([]);

  // ------------------------------------
  // Handle component initialisation
  // ------------------------------------
  const getWorkflows = async () => {
    const wfs = await requestAPI<any>('workflows');
    setWorkflows(Object.values(wfs));
  };

  useEffect(() => {
    getWorkflows();
  }, []);

  if (workflows.length === 0) {
    return (
      <div className={`workflows-list ${className}`}>
        <StyledEmptyPanel body="No workflows installed" icon={faFolderOpen} />
      </div>
    );
  }

  return (
    <div className={`workflows-list ${className}`}>
      <ul>
        {workflows.map((Item: Workflow) => (
          <li>
            <div className="workflow">
              <Link className="workflow-link" to={`/workflows/${Item.name}`}>
                <div className="workflow-header">
                  <FontAwesomeIcon icon={faDna} />
                </div>
                <div className="workflow-details">
                  <div className="workflow-name">
                    <p className="preheader">Workflow name</p>
                    <h3 className="large">{Item.name}</h3>
                  </div>
                  <div className="workflow-version">
                    <p className="preheader">Workflow version</p>
                    <h4>{Item.defaults.wfversion}</h4>
                  </div>
                </div>
              </Link>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledWorkflowsList = styled(WorkflowsList)`
  && {
    max-width: calc(1024px + 30px);
    padding: 0 15px 15px 15px;
    margin: 0 auto;
    box-sizing: border-box;
  }

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }

  .workflow {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }

  .workflow-header {
    box-sizing: border-box;
    width: 100%;
    padding: 25px 25px 0;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    border-radius: 4px;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
  }

  .workflow-header svg {
    padding: 15px 16px;
    border-radius: 50px;
    background-color: transparent;
    border: 2px solid #00485b;
    color: #00485b;
  }

  .workflow-details {
    padding: 25px 25px 25px 25px;
    text-align: left;
  }

  .workflow-details p {
    padding: 0 0 5px 0;
    color: #ccc;
  }

  .workflow-name {
    padding: 0 0 10px 0;
    margin: 0 0 15px 0;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-bottom: 1px solid #f2f2f2;
  }
`;

export default StyledWorkflowsList;
