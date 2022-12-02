import { React, useEffect, useState } from 'react'
import moment from "moment";
import "./PublishedAgo.css";

export default function PublishedAgo(props) {
    moment.updateLocale('en', {
        relativeTime: {
          future : 'in %s',
          past   : `%s${props.explore ? '' : ' ago'}`,
          s  : '%ds',
          m  : '1min',
          mm : '%dmin',
          h  : '1h',
          hh : '%dh',
          d  : '1d',
          dd : '%dd',
          M  : '1mo',
          MM : '%dmo',
          y  : '1y',
          yy : '%dy'
        }
      });
    const [publishedAgo, setPublishedAgo] = useState(moment(props.published).fromNow());
    useEffect(() => {
        const timer = setInterval(() => {
            // update every minute
            setPublishedAgo(moment(props.published).fromNow());
        }, 60 * 1000);
        return () => {
            clearInterval(timer);
        }
    }, [])

  return (
    <div className='published-ago' >· {publishedAgo}</div>
  )
}
