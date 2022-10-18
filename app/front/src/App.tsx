import {useEffect, useState} from 'react'
import './App.css'
import 'chartjs-adapter-date-fns'
import {
    Chart as ChartJS,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    // TimeSeriesScale,
    TimeScale
} from 'chart.js'
import {Scatter} from 'react-chartjs-2'
import _ from "lodash";

ChartJS.register(
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    // TimeSeriesScale,
    TimeScale
)

const beScales = {
    scales: {
        BTC: {
            type: 'linear' as const,
            position: 'left' as const,
        },
        ETH: {
            type: 'linear' as const,
            position: 'right' as const,
        },
    }
}
const brScales = {
    scales: {
        BNB: {
            type: 'linear' as const,
            position: 'left' as const,
        },
        RUB: {
            type: 'linear' as const,
            position: 'right' as const,
        },
    }
}

const options = {
    showLine: true,
    scales: {
        x: {
            // type: 'timeseries' as const,
            type: 'time' as const,
        },
    },
}

const beOpts = _.merge(options, beScales)
const brOpts = _.merge(options, brScales)

const evtSource = new EventSource("http://127.0.0.1:8000/sse")

evtSource.onopen = (/*e*/) => console.log("Connected."/*, e*/)

evtSource.addEventListener("ping", (event) => console.log(`ping: ${event.data}`))

evtSource.onerror = () => console.error("EventSource failed:")

let init = {
    USDTRUBf: [],
    USDTRUBt: [],
    BUSDRUBf: [],
    BUSDRUBt: [],

    BTCRUBf: [],
    BTCRUBt: [],
    ETHRUBf: [],
    ETHRUBt: [],

    BNBRUBf: [],
    BNBRUBt: [],
    RUBRUBf: [],
    RUBRUBt: [],
}

const fresh = (pArr: any) => {
    if (pArr.length > 1 && pArr[0].x < Date.now()-60*60*1000) {
        pArr.shift();
        fresh(pArr)
    }
}

export function App() {
    const [points, setPoints] = useState(init)

    const usd = {
        datasets: [
            {
                label: 'USDT/RUB Buy',
                data: points.USDTRUBf,
                borderColor: 'rgb(53, 162, 235)',
            },
            {
                label: 'BUSD/RUB Buy',
                data: points.BUSDRUBf,
                borderColor: 'blue',
            },
            {
                label: 'USDT/RUB Sell',
                data: points.USDTRUBt,
                borderColor: 'rgb(255, 112, 73)',
            },
            {
                label: 'BUSD/RUB Sell',
                data: points.BUSDRUBt,
                borderColor: 'red',
            },
        ],
    }
    const btceth = {
        datasets: [
            {
                label: 'BTC/RUB Buy',
                data: points.BTCRUBf,
                borderColor: 'rgb(53, 162, 235)',
                yAxisID: 'BTC',
            },
            {
                label: 'ETH/RUB Buy',
                data: points.ETHRUBf,
                borderColor: 'blue',
                yAxisID: 'ETH',
            },
            {
                label: 'BTC/RUB Sell',
                data: points.BTCRUBt,
                borderColor: 'rgb(255, 112, 73)',
                yAxisID: 'BTC',
            },
            {
                label: 'ETH/RUB Sell',
                data: points.ETHRUBt,
                borderColor: 'red',
                yAxisID: 'ETH',
            },
        ],
    }
    const bnbrub = {
        datasets: [
            {
                label: 'BNB/RUB Buy',
                data: points.BNBRUBf,
                borderColor: 'rgb(53, 162, 235)',
                yAxisID: 'BNB',
            },
            {
                label: 'RUB/RUB Buy',
                data: points.RUBRUBf,
                borderColor: 'blue',
                yAxisID: 'RUB',
            },
            {
                label: 'BNB/RUB Sell',
                data: points.BNBRUBt,
                borderColor: 'rgb(255, 112, 73)',
                yAxisID: 'BNB',
            },
            {
                label: 'RUB/RUB Sell',
                data: points.RUBRUBt,
                borderColor: 'red',
                yAxisID: 'RUB',
            },
        ],
    }

    evtSource.onmessage = (event) => {
        const nd = JSON.parse(event.data)
        const pc = structuredClone(points)
        for (const k in pc) {
            if (nd[k]) { // at least 1 new point received
                if (pc[k].length > 1) { // old points exists in chart
                    if (pc[k].slice(-1)[0].y == nd[k][0].y) { // the last point in chart == new received point
                        pc[k].pop() //todo: prev-prev point check
                    }
                    fresh(pc[k])
                }
                pc[k].push(...nd[k])
            }
        }
        setPoints(pc)
    }

    useEffect(() => {
        // console.log(points)
    }, [points]);

    return <div>
        <Scatter options={options} data={usd}/>
        <Scatter options={beOpts} data={btceth}/>
        <Scatter options={brOpts} data={bnbrub}/>
    </div>;
}
