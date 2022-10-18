import {useEffect, useState} from 'react'
import './App.css'
import 'chartjs-adapter-date-fns'
import {
    Chart as ChartJS,
    CategoryScale,
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
    CategoryScale,
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
            display: true,
            position: 'left' as const,
        },
        ETH: {
            type: 'linear' as const,
            display: true,
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
            time: {
                // minUnit: 'second' as const,
            },
        },
    },
}

const beOpts = _.merge(options, beScales)

const evtSource = new EventSource("http://127.0.0.1:8000/sse")

evtSource.onopen = (e) => console.log("Connected.", e)

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

    evtSource.onmessage = (event) => {
        const nd = JSON.parse(event.data)
        const pc = structuredClone(points)
        for (const k in pc) {
            if (pc[k].length && pc[k].slice(-1)[0].y == nd[k][0].y) {
                pc[k].pop()
            }
            pc[k].push(...nd[k])
        }
        setPoints(pc)
    }

    useEffect(() => {
        console.log(points)
    }, [points]);

    return <div>
        <Scatter options={options} data={usd}/>
        <Scatter options={beOpts} data={btceth}/>
    </div>;
}
