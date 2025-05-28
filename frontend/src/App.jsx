import {useEffect, useState} from 'react';
import {Table, Tabs, List, Typography, ConfigProvider, theme} from 'antd';
import 'antd/dist/reset.css';
import '../src/scss/main.css';
import '../src/scss/animatedBackground.css';
import columnLabels from "./columnLabels.js";
import Loader from "./components/Loader.jsx";

const {TabPane} = Tabs;

function App() {
    const [rawData, setRawData] = useState([]);
    const [processedData, setProcessedData] = useState([]);
    const [rawOnlyKeys, setRawOnlyKeys] = useState([]);
    const [processedOnlyKeys, setProcessedOnlyKeys] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAll = async () => {
            try {
                const [rawRes, processedRes] = await Promise.all([
                    fetch('http://localhost:8000/raw_data'),
                    fetch('http://localhost:8000/processed_data'),
                    // fetch('http://localhost:8000/raw_data?limit=50'),
                    // fetch('http://localhost:8000/processed_data?limit=50'),
                ]);

                const [rawJson, processedJson] = await Promise.all([
                    rawRes.json(),
                    processedRes.json(),
                ]);

                setRawData(rawJson);
                setProcessedData(processedJson);
                setLoading(false);
            } catch (err) {
                console.error("Fetch error:", err);
                setLoading(false);
            }
        };

        fetchAll();
    }, []);


    useEffect(() => {
        if (rawData.length && processedData.length) {
            const rawKeys = Object.keys(rawData[0]);
            const processedKeys = Object.keys(processedData[0]);

            setRawOnlyKeys(rawKeys.filter(k => !processedKeys.includes(k)));
            setProcessedOnlyKeys(processedKeys.filter(k => !rawKeys.includes(k)));
        }
    }, [rawData, processedData]);

    const generateColumns = (data) =>
        Object.keys(data[0] || {}).map((key) => ({
            title: columnLabels[key] || key,
            dataIndex: key,
            key,
        }));


    return (
        <ConfigProvider
            theme={{
                algorithm: theme.darkAlgorithm,
            }}
        >
            <main className="main-container">
                <Typography.Title level={2}>League Of Legends Data</Typography.Title>
                {loading ? (
                    <Loader/>
                ) : (
                    <Tabs defaultActiveKey="1">
                        <TabPane tab="Raw Data" key="1">
                            <Table
                                dataSource={rawData.map((item, index) => ({...item, key: index}))}
                                columns={generateColumns(rawData)}
                                scroll={{x: 'max-content'}}
                                bordered
                                pagination={{
                                    pageSize: 12,
                                    showSizeChanger: false,
                                }}
                            />
                        </TabPane>

                        <TabPane tab="Processed Data" key="2">
                            <Table
                                dataSource={processedData.map((item, index) => ({...item, key: index}))}
                                columns={generateColumns(processedData)}
                                scroll={{x: 'max-content'}}
                                bordered
                                // pagination={false}
                                pagination={{
                                    pageSize: 12,
                                    showSizeChanger: false,
                                }}
                            />
                        </TabPane>

                        <TabPane tab="Differences" key="3">
                            <Typography.Title level={4}>Removed in Processed Data</Typography.Title>
                            <List
                                bordered
                                dataSource={rawOnlyKeys}
                                renderItem={(item) => <List.Item>❌ {item}</List.Item>}
                            />

                            <Typography.Title level={4}>
                                Added in Processed Data
                            </Typography.Title>
                            <List
                                bordered
                                dataSource={processedOnlyKeys}
                                renderItem={(item) => <List.Item>🆕 {item}</List.Item>}
                            />
                        </TabPane>
                    </Tabs>
                )}
            </main>
        </ConfigProvider>
    );
}

export default App;
