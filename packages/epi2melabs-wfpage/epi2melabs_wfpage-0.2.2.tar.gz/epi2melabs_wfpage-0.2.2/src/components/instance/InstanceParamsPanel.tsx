import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import StyledLoadingSpinner from '../common/LoadingSpinner';
import { requestAPI } from '../../handler';
import styled from 'styled-components';
import { Instance } from './types';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IInstanceParamsPanel {
  className?: string;
  instanceData: Instance;
}

const InstanceParamsPanel = ({
  className,
  instanceData
}: IInstanceParamsPanel): JSX.Element => {
  const navigate = useNavigate();
  const routerParams = useParams();
  const [instanceParams, setInstanceParams] = useState<string[] | null>(null);

  // ------------------------------------
  // Handle instance initialisation
  // ------------------------------------
  useEffect(() => {
    getInstanceParams(instanceData);
  }, []);

  // ------------------------------------
  // Get instance params / logs / outputs
  // ------------------------------------
  const getInstanceParams = async (instanceData: Instance | null) => {
    if (instanceData) {
      const encodedPath = encodeURIComponent(
        `${instanceData.path}/params.json`
      );
      const { contents } = await requestAPI<any>(
        `file/${encodedPath}?contents=true`
      );
      if (contents !== null) {
        setInstanceParams(contents);
      }
    }
  };

  // ------------------------------------
  // Handle retry workflow
  // ------------------------------------
  const handleRerunWorkflow = () => {
    if (instanceData) {
      navigate(`/workflows/${instanceData.workflow}/${instanceData.id}`);
    }
  };

  // ------------------------------------
  // Tabbed interface
  // ------------------------------------
  return (
    <div className={`instance-params ${className}`}>
      <div className="instance-params-header">
        <h3>Instance params</h3>
        <div className="instance-section-header-controls">
          <button onClick={() => handleRerunWorkflow()}>Rerun workflow</button>
        </div>
      </div>
      <div className="instance-params-details">
        <ul>
          <li>
            <div>
              <p className="preheader">Created at</p>
              <h4>{instanceData.updated_at}</h4>
            </div>
          </li>
          <li>
            <div>
              <p className="preheader">Unique ID</p>
              <h4>{routerParams.id}</h4>
            </div>
          </li>
        </ul>
      </div>
      <div className="instance-params-items">
        {instanceParams && instanceParams.length ? (
          <ul>
            {instanceParams.map(Item => (
              <li>
                <p>{Item}</p>
              </li>
            ))}
          </ul>
        ) : (
          <div>
            <StyledLoadingSpinner />
          </div>
        )}
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledInstanceParamsPanel = styled(InstanceParamsPanel)`
  && {
    border-radius: 4px;
    padding: 25px;
    margin: 0 0 50px 0;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    background-color: white;
  }

  .instance-params-header {
    padding-bottom: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .instance-params-header button {
    margin-left: 15px;
    padding: 10px 24px;
    border-radius: 4px;
    border: none;
    font-weight: 500;
    font-size: 13px;
    line-height: 1em;
    transition: 0.2s ease-in-out all;
    background-color: #eee;
    cursor: pointer;
  }

  .instance-params-details ul li {
    padding: 15px 0 0 0;
    margin: 0 0 15px 0;
    text-align: left;
    border-top: 1px solid #f2f2f2;
  }

  .instance-params-details ul li p {
    padding: 0 0 5px 0;
    color: #ccc;
  }

  .instance-params-items {
    max-height: 500px;
    overflow-y: scroll;
    padding: 15px;
    background-color: #f4f4f4;
    border-radius: 4px;
  }

  .instance-params-items p {
    font-family: monospace;
  }
`;

export default StyledInstanceParamsPanel;
