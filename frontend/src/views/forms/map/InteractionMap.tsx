'use client';

import { useState } from 'react';

// material-ui
import Checkbox from '@mui/material/Checkbox';
import ControlPanel from 'ui-component/third-party/map/ControlPanel';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormGroup from '@mui/material/FormGroup';
import Box from '@mui/material/Box';

// third party
import { StyleSpecification } from 'maplibre-gl';
import { RMap, RNavigationControl, RGeolocateControl, RFullscreenControl, RScaleControl } from 'maplibre-react-components';

// project imports
import osm_bright from './map-data/osm_bright.json';

const interactionList = [
  { key: 'dragPan', label: 'Drag Pan' },
  { key: 'scrollZoom', label: 'Scroll Zoom' },
  { key: 'boxZoom', label: 'Box Zoom' },
  { key: 'dragRotate', label: 'Drag Rotate' },
  { key: 'doubleClickZoom', label: 'Double Click Zoom' },
  { key: 'touchZoomRotate', label: 'Touch Zoom Rotate' },
  { key: 'keyboard', label: 'Keyboard Navigation' }
];

// ==============================|| MAPLIBRE - INTERACTION ||============================== //

export default function InteractionMap() {
  const [interactions, setInteractions] = useState(
    Object.fromEntries(interactionList.map((i) => [i.key, true])) as Record<(typeof interactionList)[number]['key'], boolean>
  );

  const toggle = (key: keyof typeof interactions) => {
    setInteractions((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <Box sx={{ height: 1 }}>
      <RMap initialCenter={[72.8, 21.1]} initialZoom={4} mapStyle={osm_bright as StyleSpecification} {...interactions}>
        <RGeolocateControl position="top-left" />
        <RFullscreenControl position="top-left" />
        <RNavigationControl position="top-left" />
        <RScaleControl position="bottom-left" />
      </RMap>

      <ControlPanel>
        <FormGroup>
          {interactionList.map((item) => (
            <FormControlLabel
              key={item.key}
              control={<Checkbox checked={interactions[item.key]} onChange={() => toggle(item.key)} />}
              label={item.label}
            />
          ))}
        </FormGroup>
      </ControlPanel>
    </Box>
  );
}
