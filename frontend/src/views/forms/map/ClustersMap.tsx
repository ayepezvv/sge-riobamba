'use client';

// material-ui
import { useColorScheme, useTheme } from '@mui/material/styles';

// third-party
import { StyleSpecification } from 'maplibre-gl';
import { RMap, RLayer, RSource } from 'maplibre-react-components';

// project imports
import osm_bright from './map-data/osm_bright.json';

// types
import type { CircleLayerSpecification, SymbolLayerSpecification } from 'maplibre-gl';

// ==============================|| MAPLIBRE - CLUSTERS MAP ||============================== //

export default function ClustersMap() {
  const theme = useTheme();
  const { colorScheme } = useColorScheme();

  const scheme = colorScheme ?? 'light';
  const schemeTheme = theme.colorSchemes?.[scheme];

  const currentPalette = schemeTheme ? schemeTheme.palette : theme.palette;

  const clusterLayer: CircleLayerSpecification = {
    id: 'clusters',
    type: 'circle',
    source: 'earthquakes',
    filter: ['has', 'point_count'],
    paint: {
      'circle-color': [
        'step',
        ['get', 'point_count'],
        currentPalette.primary[200],
        100,
        currentPalette.secondary[200],
        750,
        currentPalette.warning.main
      ],
      'circle-radius': ['step', ['get', 'point_count'], 20, 100, 30, 750, 40]
    }
  };

  const clusterCountLayer: SymbolLayerSpecification = {
    id: 'cluster-count',
    type: 'symbol',
    source: 'earthquakes',
    filter: ['has', 'point_count'],
    layout: {
      'text-field': ['get', 'point_count_abbreviated'],
      'text-size': 12
    }
  };

  const unclusteredPointLayer: CircleLayerSpecification = {
    id: 'unclustered-point',
    type: 'circle',
    source: 'earthquakes',
    filter: ['!', ['has', 'point_count']],
    paint: {
      'circle-color': currentPalette.primary[200],
      'circle-radius': 4,
      'circle-stroke-width': 1,
      'circle-stroke-color': '#FFFFFF'
    }
  };

  return (
    <RMap initialCenter={[-0.5, 47.5]} initialZoom={1} mapStyle={osm_bright as StyleSpecification}>
      <RSource
        id="earthquakes"
        type="geojson"
        data="https://maplibre.org/maplibre-gl-js/docs/assets/earthquakes.geojson"
        cluster={true}
        clusterRadius={50}
      />
      <RLayer {...clusterLayer} />
      <RLayer {...clusterCountLayer} />
      <RLayer {...unclusteredPointLayer} />
    </RMap>
  );
}
