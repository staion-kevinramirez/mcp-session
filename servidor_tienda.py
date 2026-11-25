"""
Mi primer servidor MCP con FastMCP: una tienda pequeña.

Instalación:
    pip install fastmcp ó uv add fastmcp

Ejecutar (modo local, para Claude Desktop / Cursor):
    python servidor_tienda.py uv run servidor_tienda.py

Probar en el navegador con el inspector de MCP:
    fastmcp dev inspector servidor_tienda.py ó uv run fastmcp dev inspector servidor_tienda.py

Instalarlo en Claude Desktop con un solo comando:
    fastmcp install claude-desktop servidor_tienda.py ó uv run fastmcp install claude-desktop servidor_tienda.py
"""

from fastmcp import FastMCP

# 1. Crear el servidor (el nombre es lo que verá la IA)
mcp = FastMCP("Mi Tienda")

# Datos de ejemplo (en un negocio real vendrían de una base de datos o Google Sheets)
inventario = {
    "camiseta": {"precio": 45000, "stock": 12},
    "gorra": {"precio": 30000, "stock": 0},
    "taza": {"precio": 18000, "stock": 25},
}
pedidos = []


# 2. HERRAMIENTAS (tools): acciones que la IA puede ejecutar.
#    El docstring es clave: es lo que la IA lee para saber cuándo usarla.


@mcp.tool
def registrar_pedido(cliente: str, producto: str, cantidad: int) -> str:
    """Registra un pedido de un cliente y descuenta las unidades del inventario."""
    item = inventario.get(producto.lower())
    if not item:
        return f"El producto '{producto}' no existe."
    if item["stock"] < cantidad:
        return f"Solo quedan {item['stock']} unidades de {producto}."
    item["stock"] -= cantidad
    total = item["precio"] * cantidad
    pedidos.append(
        {"cliente": cliente, "producto": producto, "cantidad": cantidad, "total": total}
    )
    return f"Pedido registrado para {cliente}: {cantidad} x {producto} = ${total:,} COP"


# 3. RECURSOS (resources): información que la IA puede leer.


@mcp.resource("tienda://pedidos")
def ver_pedidos() -> list:
    """Lista de todos los pedidos registrados."""
    return pedidos


# 4. PROMPTS: plantillas reutilizables para el usuario.


@mcp.prompt
def resumen_del_dia() -> str:
    """Pide a la IA un resumen de ventas e inventario."""
    return "Revisa los pedidos y el stock de cada producto. Dame un resumen de ventas y avísame qué debo reabastecer."


# 5. Arrancar el servidor
if __name__ == "__main__":
    mcp.run()  # local (stdio)
    # Para publicarlo en internet:  mcp.run(transport="http", port=8000)
