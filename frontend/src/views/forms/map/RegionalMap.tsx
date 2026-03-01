'use client';

// third party
import { RMap, RNavigationControl, RScaleControl } from 'maplibre-react-components';

// ==============================|| MAPLIBRE - REGIONAL MAP ||============================== //

export default function RegionalMap() {
  return (
    <RMap initialCenter={[72.8636084, 21.2335611]} initialZoom={1} mapStyle="https://demotiles.maplibre.org/style.json">
      <RNavigationControl position="top-left" />
      <RScaleControl position="bottom-left" />
    </RMap>
  );
}
