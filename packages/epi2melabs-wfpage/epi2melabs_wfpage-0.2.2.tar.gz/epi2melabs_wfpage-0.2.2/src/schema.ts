import Ajv, { ErrorObject } from 'ajv';
import { GenericObject, GenericStringObject } from './types';

export function validateSchema(
  data: GenericObject,
  schema: GenericObject
): any {
  // Slower, todo: manage workflow schemas
  // and use ajv singleton
  const ajv = new Ajv({
    allErrors: true,
    strictSchema: false,
    verbose: true
  });
  const validate = ajv.compile(schema);
  const valid = validate(data);
  return { valid, errors: validate.errors };
}

export const parseValidationErrors = (
  errors: ErrorObject[]
): { [key: string]: string[] } => {
  const errorMapping: { [key: string]: string[] } = {};
  errors.forEach(Error => {
    Object.values(Error.params as GenericStringObject).forEach(key => {
      errorMapping[key] = [...(errorMapping[key] || []), Error.message || ''];
    });
  });
  return errorMapping;
};
