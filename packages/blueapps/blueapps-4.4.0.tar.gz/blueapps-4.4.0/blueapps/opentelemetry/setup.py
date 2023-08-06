# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import os

from django.conf import settings

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace.sampling import _KNOWN_SAMPLERS
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from blueapps.opentelemetry.instrumentor import BKAppInstrumentor
from blueapps.opentelemetry.metrics.instrumentor import SaaSMetricsInstrumentor


def setup_trace_config(
    service_name: str,
    bk_data_id: int,
    otel_sampler: str,
    otel_grpc_host: str,
    bk_data_token: str = "",
):
    if settings.ENVIRONMENT == "dev":
        # local environment, use jaeger as trace service
        # docker run -p 16686:16686 -p 6831:6831/udp jaegertracing/all-in-one
        trace.set_tracer_provider(
            TracerProvider(resource=Resource.create({SERVICE_NAME: service_name}))
        )
        jaeger_exporter = JaegerExporter(
            agent_host_name="localhost",
            agent_port=6831,
            udp_split_oversized_batches=True,
        )
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(jaeger_exporter)
        )
    else:
        # stage and prod environment, use bk_log as trace service
        trace.set_tracer_provider(
            tracer_provider=TracerProvider(
                resource=Resource.create(
                    {
                        "service.name": service_name,
                        "bk_data_id": bk_data_id,
                        "bk.data.token": bk_data_token,
                    },
                ),
                sampler=_KNOWN_SAMPLERS[otel_sampler],
            )
        )
        otlp_exporter = OTLPSpanExporter(endpoint=otel_grpc_host)
        span_processor = BatchSpanProcessor(otlp_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)


def setup_by_settings():
    enable_trace = os.getenv("ENABLE_TRACE", False) or getattr(
        settings, "ENABLE_OTEL_TRACE", False
    )
    if enable_trace:
        service_name = (
            os.getenv("BKAPP_OTEL_SERVICE_NAME")
            or getattr(settings, "BKAPP_OTEL_SERVICE_NAME", None)
            or settings.APP_CODE
        )
        bk_data_id = int(
            os.getenv("BKAPP_OTEL_BK_DATA_ID")
            or getattr(settings, "BKAPP_OTEL_BK_DATA_ID", -1)
        )
        otel_sampler = (
            os.getenv("BKAPP_OTEL_SAMPLER")
            or getattr(settings, "BKAPP_OTEL_SAMPLER", None)
            or "parentbased_always_off"
        )
        otel_grpc_host = os.getenv("BKAPP_OTEL_GRPC_HOST") or getattr(
            settings, "BKAPP_OTEL_GRPC_HOST", None
        )
        otel_bk_data_token = os.getenv("BKAPP_OTEL_BK_DATA_TOKEN") or getattr(
            settings, "BKAPP_OTEL_BK_DATA_TOKEN", ""
        )
        setup_trace_config(
            service_name,
            bk_data_id,
            otel_sampler,
            otel_grpc_host,
            bk_data_token=otel_bk_data_token,
        )
        BKAppInstrumentor().instrument()
    if os.getenv("ENABLE_METRICS", False):
        SaaSMetricsInstrumentor().instrument()
