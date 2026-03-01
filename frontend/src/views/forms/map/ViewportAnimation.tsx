'use client';

import { useRef } from 'react';

// material-ui
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';

// third party
import type maplibregl from 'maplibre-gl';
import { RMap, RFullscreenControl, RGeolocateControl, RNavigationControl, RScaleControl } from 'maplibre-react-components';

// project imports
import ControlPanel from 'ui-component/third-party/map/ControlPanel';

const locations: Record<string, [number, number]> = {
  india: [78.9629, 20.5937],
  russia: [105.3188, 61.524],
  canada: [-106.3468, 56.1304],
  america: [-98.5795, 39.8283],
  australia: [133.7751, -25.2744],
  africa: [21.7587, 1.9579],
  china: [104.1954, 35.8617]
};

// ==============================|| MAPLIBRE - VIEWPORT ANIMATION ||============================== //

export default function ViewportAnimation() {
  const mapRef = useRef<maplibregl.Map | null>(null);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const city = event.target.value;
    const coords = locations[city];
    if (!coords) return;

    const map = mapRef.current;
    if (!map) return;

    map.flyTo({
      center: coords,
      zoom: 4,
      speed: 0.8,
      curve: 1.5,
      essential: true
    });
  };

  return (
    <>
      <ControlPanel>
        <RadioGroup onChange={handleChange}>
          {locations &&
            Object.keys(locations).map((item) => (
              <FormControlLabel
                key={item}
                value={item}
                control={<Radio size="small" />}
                label={item}
                sx={{ textTransform: 'capitalize' }}
              />
            ))}
        </RadioGroup>
      </ControlPanel>

      <RMap initialAttributionControl={false} ref={mapRef}>
        <RFullscreenControl position="top-left" />
        <RGeolocateControl position="top-left" showUserLocation={true} showAccuracyCircle={true} trackUserLocation={false} />
        <RScaleControl position="bottom-left" />
        <RNavigationControl position="top-left" showCompass={true} />
      </RMap>
    </>
  );
}
