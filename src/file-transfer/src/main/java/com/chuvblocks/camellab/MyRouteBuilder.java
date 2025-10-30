package com.chuvblocks.camellab;

import org.apache.camel.Exchange;
import org.apache.camel.Processor;
import org.apache.camel.builder.RouteBuilder;

import java.util.ArrayList;
import java.util.List;

public class MyRouteBuilder extends RouteBuilder {
    @Override
    public void configure() {
        from("file:../../?noop=true&fileName=envios.csv")
            .routeId("csv-to-json-envios")
            .unmarshal().csv()
            .process(new Processor() {
                @Override
                public void process(Exchange exchange) {
                    @SuppressWarnings("unchecked")
                    List<List<?>> rows = exchange.getIn().getBody(List.class);
                    List<Envio> envios = new ArrayList<>();
                    if (rows != null && !rows.isEmpty()) {
                        int start = 0;
                        List<?> first = rows.get(0);
                        if (first != null && first.size() >= 4) {
                            Object c0 = first.get(0);
                            if (c0 != null && "id_envio".equalsIgnoreCase(String.valueOf(c0).trim())) {
                                start = 1;
                            }
                        }
                        for (int i = start; i < rows.size(); i++) {
                            List<?> r = rows.get(i);
                            if (r == null) continue;
                            String id_envio = getCell(r, 0);
                            String cliente = getCell(r, 1);
                            String direccion = getCell(r, 2);
                            String estado = getCell(r, 3);
                            if (id_envio == null && cliente == null && direccion == null && estado == null) {
                                continue;
                            }
                            envios.add(new Envio(id_envio, cliente, direccion, estado));
                        }
                    }
                    exchange.getIn().setBody(envios);
                }

                private String getCell(List<?> r, int idx) {
                    if (r.size() <= idx) return null;
                    Object v = r.get(idx);
                    if (v == null) return null;
                    String s = String.valueOf(v).trim();
                    return s.isEmpty() ? null : s;
                }
            })
            .marshal().json()
            .to("file:../data?fileName=envios.json&autoCreate=true");
    }
}
