// material-ui
import { useColorScheme } from '@mui/material/styles';
import CardMedia from '@mui/material/CardMedia';
import Link from '@mui/material/Link';

// third party
import Slider, { Settings } from 'react-slick';

// types
import { ThemeMode } from 'config';

// assets
const imageLightSlider1 = '/assets/images/landing/pre-apps/slider-light-1.png';
const imageDarkSlider1 = '/assets/images/landing/pre-apps/slider-dark-1.png';
const imageLightSlider2 = '/assets/images/landing/pre-apps/slider-light-2.png';
const imageDarkSlider2 = '/assets/images/landing/pre-apps/slider-dark-2.png';
const imageLightSlider3 = '/assets/images/landing/pre-apps/slider-light-3.png';
const imageDarkSlider3 = '/assets/images/landing/pre-apps/slider-dark-3.png';

// ================================|| SLIDER - ITEMS ||================================ //

function Item({ item }: { item: { image: string } }) {
  return <CardMedia component="img" image={item.image} title="Slider5 image" />;
}

// ================================|| SLIDER ||================================ //

export default function ComingSoonSlider({ handleClickOpen }: { handleClickOpen: (slideIndex: number) => void }) {
  const settings: Settings = {
    autoplay: true,
    arrows: false,
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1
  };
  const { colorScheme } = useColorScheme();

  const imageSlider1 = colorScheme === ThemeMode.DARK ? imageDarkSlider1 : imageLightSlider1;
  const imageSlider2 = colorScheme === ThemeMode.DARK ? imageDarkSlider2 : imageLightSlider2;
  const imageSlider3 = colorScheme === ThemeMode.DARK ? imageDarkSlider3 : imageLightSlider3;

  const items = [{ image: imageSlider1 }, { image: imageSlider2 }, { image: imageSlider3 }];

  return (
    <Slider {...settings}>
      {items.map((item, index) => (
        <Link key={index} href="#" variant="inherit" sx={{ cursor: 'pointer' }} onClick={() => handleClickOpen(index)}>
          <Item item={item} />
        </Link>
      ))}
    </Slider>
  );
}
