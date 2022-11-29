export api_key_aws=3zFifoikZad4SDRLJFsoVX9F
export api_key_intel=3zFifoikZad4SDRLJFsoVX9F
export conn_addr_aws=inference-33-1.aaorm9bej4xwhihmdknjw5e.cloud.cnvrg.io
export conn_addr_intel=inference-33-1.aaorm9bej4xwhihmdknjw5e.cloud.cnvrg.io
export conn_req_aws=/api/v1/endpoints/p6ktydnwfegxf8azpano
export conn_req_intel=/api/v1/endpoints/p6ktydnwfegxf8azpano
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
maxUploadSize=1028\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" >> ~/.streamlit/config.toml
