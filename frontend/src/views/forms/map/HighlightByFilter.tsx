'use client';

import { useState, useEffect } from 'react';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';
import Typography from '@mui/material/Typography';

// third party
import { MapLayerMouseEvent } from 'maplibre-gl';
import { RMap, RSource, RLayer, RPopup } from 'maplibre-react-components';

// project imports
import SubCard from 'ui-component/cards/SubCard';

// ==============================|| MAPLIBRE - HIGHLIGHT BY FILTER WITH TOOLTIP ||============================== //

export default function HighlightByFilter() {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();

  const scheme = colorScheme ?? 'light';
  const schemeTheme = theme.colorSchemes?.[scheme];

  const currentPalette = schemeTheme ? schemeTheme.palette : theme.palette;

  const [popup, setPopup] = useState<{ lng: number; lat: number; name: string } | null>(null);
  const [highlightState, setHighlightState] = useState<string | null>('Gujarat');

  useEffect(() => {
    setPopup({ lng: 71.57, lat: 23.02, name: 'Gujarat' });
  }, []);

  function handleClick(e: MapLayerMouseEvent) {
    const features = e.target.queryRenderedFeatures(e.point, { layers: ['states-layer'] });

    if (features.length > 0) {
      const stateName = features[0].properties?.NAME_1 || 'Unknown';
      setPopup({ lng: e.lngLat.lng, lat: e.lngLat.lat, name: stateName });
      setHighlightState(stateName);
    } else {
      setPopup(null);
      setHighlightState(null);
    }
  }

  return (
    <RMap
      initialZoom={3.5}
      initialCenter={[80.9629, 20.5937]}
      onClick={handleClick}
      mapStyle="https://openmaptiles.geo.data.gouv.fr/styles/osm-bright/style.json"
    >
      <RSource id="states" type="geojson" data="https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson" />
      <RLayer id="states-layer" type="fill" source="states" paint={{ 'fill-color': currentPalette.primary.light, 'fill-opacity': 0.2 }} />
      <RLayer id="states-outline" type="line" source="states" paint={{ 'line-color': currentPalette.primary[200], 'line-width': 1.2 }} />

      {highlightState && (
        <RLayer
          id="highlight-layer"
          type="fill"
          source="states"
          paint={{ 'fill-color': currentPalette.secondary.main, 'fill-opacity': 0.6 }}
          filter={['==', 'NAME_1', highlightState]}
        />
      )}

      {popup && (
        <RPopup longitude={popup.lng} latitude={popup.lat}>
          <SubCard sx={{ borderWidth: 0 }} contentSX={{ p: 1, '&:last-child': { pb: 1 } }}>
            <Typography variant="h5">{popup.name}</Typography>
          </SubCard>
        </RPopup>
      )}
    </RMap>
  );
}
