package com.chuvblocks.camellab;

public class Envio {
    private String id_envio;
    private String cliente;
    private String direccion;
    private String estado;

    public Envio() {}

    public Envio(String id_envio, String cliente, String direccion, String estado) {
        this.id_envio = id_envio;
        this.cliente = cliente;
        this.direccion = direccion;
        this.estado = estado;
    }

    public String getId_envio() { return id_envio; }
    public void setId_envio(String id_envio) { this.id_envio = id_envio; }

    public String getCliente() { return cliente; }
    public void setCliente(String cliente) { this.cliente = cliente; }

    public String getDireccion() { return direccion; }
    public void setDireccion(String direccion) { this.direccion = direccion; }

    public String getEstado() { return estado; }
    public void setEstado(String estado) { this.estado = estado; }
}

