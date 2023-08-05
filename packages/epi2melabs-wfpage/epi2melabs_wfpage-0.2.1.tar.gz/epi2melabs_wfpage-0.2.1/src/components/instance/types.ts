export type InstanceParams = {
  [key: string]: string;
};

export type Instance = {
  id: string;
  path: string;
  name: string;
  status: string;
  workflow: string;
  created_at: string;
  updated_at: string;
  params: InstanceParams;
};
