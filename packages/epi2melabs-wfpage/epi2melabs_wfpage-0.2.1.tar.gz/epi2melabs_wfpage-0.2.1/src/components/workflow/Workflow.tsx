import React, { useEffect, useState } from 'react';
import { requestAPI } from '../../handler';
import { useParams, useNavigate } from 'react-router-dom';
import { GenericObject } from '../../types';
import StyledTabbedHeader from '../common/TabbedHeader';
import { validateSchema, parseValidationErrors } from '../../schema';
import StyledWorkflowLaunchPanel from './WorkflowLaunchPanel';
import StyledWorkflowDocsPanel from './WorkflowDocsPanel';
import styled from 'styled-components';
import {
  Workflow,
  WorkflowDefaults,
  ParameterSection,
  Parameter
} from './types';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IWorkflowComponent {
  className?: string;
}

const WorkflowComponent = ({ className }: IWorkflowComponent): JSX.Element => {
  // ------------------------------------
  // Set up state
  // ------------------------------------
  const params = useParams();
  const navigate = useNavigate();
  const [workflowData, setWorkflowData] = useState<Workflow | undefined>();
  const [workflowParams, setWorkflowParams] = useState<WorkflowDefaults>({});
  const [workflowParamsValid, setWorkflowParamsValid] = useState(false);
  const [workflowParamsErrors, setWorkflowParamsErrors] =
    useState<GenericObject>({});
  const [workflowActiveSections, setWorkflowActiveSections] = useState<
    ParameterSection[]
  >([]);
  const [instanceNameError, setInstanceNameError] = useState<string | null>(
    null
  );
  const [instanceCreateError, setInstanceCreateError] = useState<string | null>(
    null
  );
  const [instanceName, setInstanceName] = useState<string | null>(null);
  const [animationClass, setAnimationClass] = useState('animated');
  const [selectedTab, setSelectedTab] = useState(0);

  // ------------------------------------
  // Handle component initialisation
  // ------------------------------------
  const getWorkflowData = async () => {
    return await requestAPI<any>(`workflows/${params.name}`);
  };

  const getInstanceParams = async (instance_id: string | undefined) => {
    if (instance_id) {
      const { path } = await requestAPI<any>(`instances/${instance_id}`);
      const encodedPath = encodeURIComponent(`${path}/params.json`);
      const { exists, contents } = await requestAPI<any>(
        `file/${encodedPath}?contents=true`
      );
      if (!exists) {
        return null;
      }
      return JSON.parse(contents.join(''));
    }
  };

  const filterHiddenParameters = (parameters: { [key: string]: Parameter }) =>
    Object.entries(parameters)
      .filter(([key, Property]) => !Property.hidden && key !== 'out_dir')
      .reduce(
        (obj, prop) => ({
          [prop[0]]: prop[1],
          ...obj
        }),
        {}
      );

  const getSchemaSections = (definitions: ParameterSection[]) => {
    return definitions
      .map(Section => ({
        ...Section,
        properties: filterHiddenParameters(Section.properties)
      }))
      .filter(Def => Object.keys(Def.properties).length !== 0);
  };

  const overrideDefaults = (
    sections: ParameterSection[],
    defaults: GenericObject
  ) => {
    return sections.map(Section => ({
      ...Section,
      properties: Object.entries(Section.properties).reduce(
        (obj, prop) => ({
          [prop[0]]: {
            ...prop[1],
            default: defaults[prop[0]] || prop[1].default
          },
          ...obj
        }),
        {}
      )
    }));
  };

  useEffect(() => {
    const init = async () => {
      // Get the initial workflow data
      const workflowData = await getWorkflowData();
      setWorkflowData(workflowData);
      // Acquire the workflow default params
      const defaults = await getInstanceParams(params.instance_id);
      if (defaults) {
        setWorkflowParams(defaults);
      } else {
        setWorkflowParams(workflowData.defaults);
      }
      // Get and set the workflow schema sections
      const sections = getSchemaSections(
        Object.values(workflowData.schema.definitions)
      );
      if (defaults) {
        const overriden = overrideDefaults(sections, defaults);
        setWorkflowActiveSections(overriden);
        return;
      }
      setWorkflowActiveSections(sections);
    };
    init();
  }, []);

  // ------------------------------------
  // Handle parameter validation
  // ------------------------------------
  const handleInputChange = (id: string, format: string, value: any) => {
    if (value === '') {
      const { [id]: _, ...rest } = workflowParams;
      setWorkflowParams(rest);
      return;
    }
    setWorkflowParams({ ...workflowParams, [id]: value });
  };

  useEffect(() => {
    if (workflowData) {
      const { valid, errors } = validateSchema(
        workflowParams,
        workflowData.schema
      );
      valid
        ? setWorkflowParamsErrors({})
        : setWorkflowParamsErrors(parseValidationErrors(errors));
      setWorkflowParamsValid(valid);
    }
  }, [workflowParams]);

  // ------------------------------------
  // Handle instance naming
  // ------------------------------------
  const namePattern = new RegExp('^[-0-9A-Za-z_ ]+$');
  const handleInstanceRename = (name: string) => {
    if (name === '') {
      setInstanceName(null);
      setInstanceNameError('An instance name cannot be empty');
      return;
    }
    if (!namePattern.test(name)) {
      setInstanceName(null);
      setInstanceNameError(
        'An instance name can only contain dashes, ' +
          'underscores, spaces, letters and numbers'
      );
      return;
    }
    setInstanceName(name);
    setInstanceNameError(null);
  };

  // ------------------------------------
  // Handle workflow launch
  // ------------------------------------
  const launchWorkflow = async () => {
    if (!workflowParamsValid || !instanceName) {
      return;
    }
    const { created, instance, error } = await requestAPI<any>('instances', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        workflow: params.name,
        params: workflowParams,
        ...(instanceName ? { name: instanceName } : {})
      })
    });
    if (error) {
      setInstanceCreateError(error);
    }
    if (!created) {
      return;
    }
    navigate(`/instances/${instance.id}`);
  };

  // ------------------------------------
  // Tabbed interface
  // ------------------------------------
  const tabs = [
    {
      body: 'Launch workflow',
      onClick: () => setSelectedTab(0),
      element: (
        <div
          className={`tab-contents ${animationClass}`}
          onAnimationEnd={() => setAnimationClass('')}
        >
          <StyledWorkflowLaunchPanel
            parameterSections={workflowActiveSections}
            parameterErrors={workflowParamsErrors}
            parametersValid={workflowParamsValid}
            onChangeParameter={handleInputChange}
            instanceName={instanceName}
            instanceNameError={instanceNameError}
            instanceCreateError={instanceCreateError}
            onChangeInstanceName={handleInstanceRename}
            onClickLaunch={launchWorkflow}
          />
        </div>
      )
    },
    {
      body: 'Documentation',
      onClick: () => setSelectedTab(1),
      element: (
        <div className="tab-contents animated">
          <StyledWorkflowDocsPanel docs={workflowData?.docs} />
        </div>
      )
    }
  ];

  return workflowData ? (
    <div className={`workflow ${className}`}>
      <div className="workflow-container">
        <StyledTabbedHeader
          title={workflowData.name}
          body={<p className="large">{workflowData.desc}</p>}
          active={selectedTab}
          tabs={tabs}
        />

        {tabs[selectedTab].element}
      </div>
    </div>
  ) : (
    <React.Fragment />
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledWorkflowComponent = styled(WorkflowComponent)`
  background-color: #f6f6f6;

  .workflow-container {
    box-sizing: border-box;
    padding: 0 0 50px 0 !important;
  }

  @keyframes fadeInUp {
    from {
      transform: translate3d(0, 40px, 0);
    }

    to {
      transform: translate3d(0, 0, 0);
      opacity: 1;
    }
  }

  .tab-contents {
    width: 100%;
    padding: 0 15px;
    box-sizing: border-box;
    max-width: calc(1024px + 30px);
    margin: 0 auto 25px auto;
  }

  .animated {
    opacity: 0;
    animation-name: fadeInUp;
    animation-duration: 1s;
    animation-fill-mode: both;
  }
`;

export default StyledWorkflowComponent;
