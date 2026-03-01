'use client';

import { useState, useEffect } from 'react';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';

// third party
import { Feature, FeatureCollection, Point } from 'geojson';
import { RMap, RSource, RLayer } from 'maplibre-react-components';

// project imports
import { withAlpha } from 'utils/colorUtils';

type EarthquakeFeature = Feature<Point, { time: number; mag: number; [key: string]: any }>;

type EarthquakeFeatureCollection = FeatureCollection<Point, EarthquakeFeature['properties']>;

// ==============================|| HEAT MAP ||============================== //

export default function Heatmap() {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();

  const scheme = colorScheme ?? 'light';
  const schemeTheme = theme.colorSchemes?.[scheme];

  const currentPalette = schemeTheme ? schemeTheme.palette : theme.palette;

  const [earthquakes, setEarthquakes] = useState<EarthquakeFeatureCollection | null>(null);

  useEffect(() => {
    fetch('https://maplibre.org/maplibre-gl-js/docs/assets/earthquakes.geojson')
      .then((resp) => resp.json())
      .then((json: EarthquakeFeatureCollection) => {
        const validFeatures = json.features.filter(
          (f) => f.properties && typeof f.properties.time === 'number' && typeof f.properties.mag === 'number'
        );

        setEarthquakes({
          type: 'FeatureCollection',
          features: validFeatures
        });
      })
      .catch((e) => console.error('Failed to load data', e));
  }, []);

  return (
    <RMap initialZoom={3} initialCenter={[-110, 30]} mapStyle="https://tiles.openfreemap.org/styles/bright">
      {earthquakes && <RSource id="earthquakes" type="geojson" data={earthquakes} />}
      {earthquakes && (
        <RLayer
          id="earthquakes-heat"
          type="heatmap"
          source="earthquakes"
          paint={{
            'heatmap-weight': ['interpolate', ['linear'], ['get', 'mag'], 0, 0, 6, 1],
            'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 0, 1, 9, 3],
            'heatmap-color': [
              'interpolate',
              ['linear'],
              ['heatmap-density'],
              0,
              withAlpha(currentPalette.grey[50], 0),
              0.2,
              currentPalette.primary[200],
              0.4,
              currentPalette.primary.light,
              0.6,
              currentPalette.orange.main,
              0.8,
              currentPalette.orange.dark,
              0.9,
              currentPalette.warning.main
            ],
            'heatmap-radius': ['interpolate', ['linear'], ['zoom'], 0, 2, 9, 20],
            'heatmap-opacity': ['interpolate', ['linear'], ['zoom'], 7, 1, 9, 0]
          }}
        />
      )}
    </RMap>
  );
}
