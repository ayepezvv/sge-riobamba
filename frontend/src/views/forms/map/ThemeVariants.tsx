'use client';

import { useState, useCallback } from 'react';

// material-ui
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';

// third party
import { StyleSpecification } from 'maplibre-gl';
import { RMap, RMarker, RNavigationControl, RScaleControl } from 'maplibre-react-components';

// project imports
import ControlPanel from 'ui-component/third-party/map/ControlPanel';

interface Props {
  themes: { [key: string]: StyleSpecification };
}

// ==============================|| MAPLIBRE - THEME VARIANTS ||============================== //

export default function ThemeVariants({ themes }: Props) {
  const [selectTheme, setSelectTheme] = useState('streets');

  const handleChangeTheme = useCallback((value: string) => setSelectTheme(value), []);

  return (
    <>
      <RMap initialCenter={[72.8691665, 21.2330191]} initialZoom={14} mapStyle={themes?.[selectTheme]}>
        <RMarker longitude={72.8691665} latitude={21.2330191} />
        <RNavigationControl position="top-left" />
        <RScaleControl position="bottom-left" />
      </RMap>

      <ControlPanel title="Select Variants">
        <RadioGroup
          sx={{ '.MuiTypography-root': { pt: 0.75 } }}
          value={selectTheme}
          onChange={(event, newValue) => handleChangeTheme(newValue)}
        >
          {Object.keys(themes).map((item) => (
            <FormControlLabel key={item} value={item} control={<Radio size="small" />} label={item} sx={{ textTransform: 'capitalize' }} />
          ))}
        </RadioGroup>
      </ControlPanel>
    </>
  );
}
