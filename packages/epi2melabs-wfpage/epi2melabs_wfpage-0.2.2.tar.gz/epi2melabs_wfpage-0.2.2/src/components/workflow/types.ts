export type ParameterSection = {
  title: string;
  description: string;
  type?: string;
  fa_icon?: string;
  properties: { [key: string]: Parameter };
};

export type Parameter = {
  type: string;
  description?: string;
  help_text?: string;
  hidden?: boolean;
  default?: any;
  [key: string]: any;
};

export type WorkflowDocs = {
  [key: string]: string;
};

export type WorkflowDefaults = {
  [key: string]: string;
};

export type WorkflowSchema = {
  [key: string]: any;
};

export type Workflow = {
  url: string;
  name: string;
  path: string;
  desc: string;
  schema: WorkflowSchema;
  defaults: WorkflowDefaults;
  docs: WorkflowDocs;
};
