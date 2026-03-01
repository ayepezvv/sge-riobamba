// material-ui
import Grid from '@mui/material/Grid';

// third party
import { StyleSpecification } from 'maplibre-gl';

// project imports
import ThemeVariants from './ThemeVariants';
import RegionalMap from './RegionalMap';
import MarkersPopups from './MarkersPopups';
import DraggableMarker from './DraggableMarkerMap';
import GeoJSONAnimation from './GeoJSONAnimation';
import ClustersMap from './ClustersMap';
import InteractionMap from './InteractionMap';
import ViewportAnimation from './ViewportAnimation';
import HighlightByFilter from './HighlightByFilter';
import Heatmap from './HeatMap';

import MainCard from 'ui-component/cards/MainCard';
import MapContainerStyled from 'ui-component/third-party/map/MapContainerStyled';

import { countries } from 'data/location';

import osm_bright from './map-data/osm_bright.json';
import alidade_smooth from './map-data/alidade_smooth.json';
import alidade_smooth_dark from './map-data/alidade_smooth_dark.json';

export const MAPBOX_THEMES = {
  light: alidade_smooth as StyleSpecification,
  dark: alidade_smooth_dark as StyleSpecification,
  streets: osm_bright as StyleSpecification
};

// ==============================|| MAPLIBRE - MAP ||============================== //

export default function Map() {
  return (
    <Grid container spacing={3}>
      <Grid size={12}>
        <MainCard title="Theme Variants">
          <MapContainerStyled>
            <ThemeVariants themes={MAPBOX_THEMES} />
          </MapContainerStyled>
        </MainCard>
      </Grid>
      <Grid size={12}>
        <MainCard title="Regional Map">
          <MapContainerStyled>
            <RegionalMap />
          </MapContainerStyled>
        </MainCard>
      </Grid>
      <Grid size={12}>
        <MainCard title="Markers & Popups">
          <MapContainerStyled>
            <MarkersPopups data={countries} />
          </MapContainerStyled>
        </MainCard>
      </Grid>
      <Grid size={{ xs: 12, md: 6 }}>
        <MainCard title="Draggable Marker">
          <MapContainerStyled>
            <DraggableMarker />
          </MapContainerStyled>
        </MainCard>
      </Grid>
      <Grid size={{ xs: 12, md: 6 }}>
        <MainCard title="Geo JSON Animation">
          <MapContainerStyled>
            <GeoJSONAnimation />
          </MapContainerStyled>
        </MainCard>
      </Grid>
      <Grid size={12}>
        <MainCard title="Clusters">
          <MapContainerStyled>
            <ClustersMap />
          </MapContainerStyled>
        </MainCard>
      </Grid>
      <Grid size={12}>
        <MainCard title="Interaction">
          <MapContainerStyled>
            <InteractionMap />
          </MapContainerStyled>
        </MainCard>
      </Grid>
      <Grid size={12}>
        <MainCard title="Viewport Animation">
          <MapContainerStyled>
            <ViewportAnimation />
          </MapContainerStyled>
        </MainCard>
      </Grid>
      <Grid size={{ xs: 12, md: 6 }}>
        <MainCard title="Highlight By Filter">
          <MapContainerStyled>
            <HighlightByFilter />
          </MapContainerStyled>
        </MainCard>
      </Grid>
      <Grid size={{ xs: 12, md: 6 }}>
        <MainCard title="Heatmap">
          <MapContainerStyled>
            <Heatmap />
          </MapContainerStyled>
        </MainCard>
      </Grid>
    </Grid>
  );
}
