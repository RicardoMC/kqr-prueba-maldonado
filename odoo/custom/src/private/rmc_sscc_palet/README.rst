SSCC GS1 por compañía
=====================

Este módulo genera automáticamente códigos SSCC GS1 de 18 dígitos
para los paquetes de inventario, utilizando un prefijo GS1 y una
secuencia independientes para cada compañía.

Features
========

* Configuración del prefijo GS1 en cada compañía.
* Generación automática del SSCC al crear un paquete.
* Códigos de 18 dígitos con extensión y dígito de control GS1.
* Secuencias independientes por compañía.
* Visualización del SSCC en los formularios y listas de paquetes.

Installation
============

Install the ``rmc_sscc_palet`` module.

Configuration
=============

#. Open the company configuration.
#. Set the numeric GS1 company prefix in the ``Prefijo GS1`` field.
#. Configure the prefix separately for each company.

Usage
=====

When a stock package is created, the module generates its SSCC
automatically using the configured company's prefix and sequence.

The generated SSCC is displayed on the package form and package list.
The SSCC field is read-only.

The generated code consists of the extension digit, the GS1 company
prefix, the serial reference and the GS1 Mod-10 check digit.
