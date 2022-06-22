import {Fragment} from 'react';

import {MobileVital, WebVital} from 'sentry/utils/discover/fields';
import {
  MOBILE_VITAL_DETAILS,
  WEB_VITAL_DETAILS,
} from 'sentry/utils/performance/vitals/constants';
import {Vital} from 'sentry/utils/performance/vitals/types';

type Measurement = {
  key: string;
  name: string;
};

export type MeasurementCollection = Record<string, Measurement>;

type VitalType = WebVital | MobileVital;

function measurementsFromDetails(
  details: Partial<Record<VitalType, Vital>>
): MeasurementCollection {
  return Object.fromEntries(
    Object.entries(details).map(([key, value]) => {
      const newValue: Measurement = {
        name: value.name,
        key,
      };
      return [key, newValue];
    })
  );
}

const MOBILE_MEASUREMENTS = measurementsFromDetails(MOBILE_VITAL_DETAILS);
const WEB_MEASUREMENTS = measurementsFromDetails(WEB_VITAL_DETAILS);
const CUSTOM_MEASUREMENTS = measurementsFromDetails({
  'measurements.longtaskcount': {
    slug: 'measurements.longtaskcount',
    name: 'measurements.longtaskcount',
    description: 'measurements.longtaskcount',
    type: 'number',
  },
  'measurements.total.db.calls': {
    slug: 'measurements.total.db.calls',
    name: 'measurements.total.db.calls',
    description: 'measurements.total.db.calls',
    type: 'number',
  },
} as Record<string, Vital>);

export function getMeasurements() {
  return {...WEB_MEASUREMENTS, ...MOBILE_MEASUREMENTS, ...CUSTOM_MEASUREMENTS};
}

type ChildrenProps = {
  measurements: MeasurementCollection;
};

type Props = {
  children: (props: ChildrenProps) => React.ReactNode;
};

function Measurements({children}: Props) {
  const measurements = getMeasurements();
  return <Fragment>{children({measurements})}</Fragment>;
}

export default Measurements;
