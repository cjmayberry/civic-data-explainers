# EMEL Data Platform (dados.emel.pt) — English translation reference

Translation of the Portuguese-only parts of the EMEL open-data portal, compiled
2026-08-06 from the live pages. Dataset *descriptions* on the portal are already
bilingual (PT | EN); the UI chrome, group names, and **field names** are what this
document translates.

## Portal UI / navigation
| Português | English |
| --- | --- |
| Página inicial | Home |
| Sobre | About |
| Grupos | Groups |
| Organizações | Organizations |
| Conjunto de Dados | Dataset |
| Dados e Recursos | Data & Resources |
| Explorar | Explore |
| Prévisualização | Preview |
| Transferir | Download |
| Informação Adicional | Additional Information |
| Campo / Valor | Field / Value |
| Última Atualização | Last updated |
| Data de criação | Created |
| Ordenar por | Sort by |
| Relevância | Relevance |
| Nome Ascendente / Descendente | Name A–Z / Z–A |
| Última Modificação | Last modified |
| Filtrar Resultados | Filter results |
| Procurar | Search |
| Pesquisar dados | Search data |
| (n) conjuntos de dados encontrados | (n) datasets found |

## Group (category) names
| Português | English |
| --- | --- |
| Acessibilidade | Accessibility |
| Carregamento Elétrico | Electric Charging |
| Estacionamento em Parques | Off-street parking (garages) |
| Estacionamento Via Pública | On-street parking |
| Trafégo (sic; tráfego) | Traffic |
| Ciclável | Cycling |

## Acronyms used across the parking datasets
| Term | Expansion / meaning |
| --- | --- |
| EMEL | Empresa de Mobilidade e Estacionamento de Lisboa — Lisbon Mobility & Parking Company (municipal) |
| ZEDL | Zona de Estacionamento de Duração Limitada — Limited-duration parking zone |
| ZAAC | Zona de Acesso Automóvel Condicionado — Restricted vehicle-access zone |
| GIRA | Lisbon's public shared-bike service |
| CP7 / cP7 / cp7 | 7-digit Portuguese postcode (XXXX-XXX) |

## Field names — cyclinglanes (Cycling Network)
| Field (PT) | English |
| --- | --- |
| idTrocoCiclovia | Cycle-lane segment ID |
| idCiclovia | Cycle-route ID (e.g. RC0038) |
| localizacao | Location |
| hierarquia | Hierarchy (Local / Principal = local / main) |
| via | On-road (Sim = yes) |
| passeio | Adjacent to sidewalk/pavement |
| itinerario | Itinerary |
| restricaoAcesso | Access restriction |
| situacao | Status (Operacional = operational) |
| freguesia | Parish |
| largura | Width (m) |
| comprimento | Length (m) |
| dataAbertura | Opening date |
| dataAtualizacao | Last update |
| tipo | Type (Definitiva = permanent) |
| viaDupla | Two-way lane (Bidirecional = bidirectional) |
| pavQualidade | Pavement quality (Bom / Muito Bom = good / very good) |
| GeoJSONCoordinates | Geometry (LineString) |

## Field names — girastations (GIRA stations)
| Field (PT) | English |
| --- | --- |
| id_expl | Station (exploitation) ID |
| estacaolocalizacao | Station location / name |
| latitude / longitude | Coordinates |
| horariofuncionamento | Operating hours |
| tarifario | Pricing / tariff |
| formaspagto | Payment methods |
| contatoservassistencia | Support contact |
| wifi | Wi-Fi available (True/False) |
| aberturadt | Opening date |
| criacaodtt | Record created |
| atualizacaodtt | Record updated |
| cp7 | Postcode |

## Field names — liftsandescalators (Lifts and escalators)
| Field (PT) | English |
| --- | --- |
| id | Facility ID |
| localizacao | Location |
| contacto | Contact phone |
| horario | Operating hours |
| dataEdicao | Edit date |
| freguesia | Parish |
| cP7 | Postcode |
| Latitude / Longitude | Coordinates |

## Field names — parkingregulatedzonespaces (Parking zones)
| Field (PT) | English |
| --- | --- |
| zona | Zone code (e.g. 001) |
| zonaNR | Zone name (e.g. "Berna / Valbom") |
| coordenadas | Boundaries (GeoJSON Polygon) |

## Field names — parkingzone (Parking areas)
| Field (PT) | English |
| --- | --- |
| ID | Area ID |
| Produto | Tariff product (e.g. "AmarelaRotação", "Exclusivo para residentes") |
| Cod_Tarifa | Tariff code (e.g. YB, YA) |
| Tarifa | Rate band color (Amarela = yellow, Verde = green) |
| Cod_Horario | Schedule code (e.g. H1, H5) |
| Horario | Charged hours (e.g. "2ª A 6ª 9-19H", "24 HORAS") |
| ID_Tipo_Estacionamento | Parking-type ID |
| Tipo_Estacionamento | Parking type (Rotativo = rotating/limited, Bolsa de Residentes = residents' bays) |
| Observacoes | Notes |
| GeoJSONCoordinates | Geometry (MultiPolygon) |

Note: weekday shorthand "2ª A 6ª" = Monday–Friday (2ª=segunda … 6ª=sexta).

## Field names — statisticsplacesbytypologyandparish (Parking stats)
| Field (PT) | English |
| --- | --- |
| freguesia | Parish |
| tipologia | Type of space (e.g. "Carga Veículos Eléctricos" = EV charging, "Cargas e Descargas" = loading/unloading) |
| lugaresQTD | Number of spaces (quantity) |

## Field names — tunnels (Road tunnels)
| Field (PT) | English |
| --- | --- |
| tunelID | Tunnel ID |
| localizacao | Location |
| latitude / longitude | Coordinates |
| condicaoAcesso | Access conditions (speed limit, max height, vehicle bans) |
| pertubacoes (sic; perturbações) | Disruptions / traffic restrictions link |
| cP7 | Postcode |
| freguesia | Parish |
| cadastradoEm | Registered on (date) |

## Sample values glossary
| Value (PT) | English |
| --- | --- |
| Situacao: Operacional | Status: operational |
| Hierarquia: Local / Principal | Hierarchy: local / main |
| Tipo: Definitiva | Type: permanent |
| ViaDupla: Bidirecional | Two-way: bidirectional |
| PavQualidade: Bom / Muito Bom | Pavement: good / very good |
| Tipo_Estacionamento: Rotativo | Parking type: rotating (limited time) |
| Tipo_Estacionamento: Bolsa de Residentes | Parking type: residents' bays |
| Tarifa: Amarela / Verde | Rate band: yellow / green |
| "2ª A 6ª 9-19H" | Mon–Fri 9am–7pm |
| "24 HORAS" | 24 hours |
| Anual: 25€ / Mensal: 15€ / Diário: 2€ | Annual €25 / monthly €15 / daily €2 |
| Caução de 300€ | €300 deposit (occasional GIRA users) |
| Vel. Máx. 50 Km/h | Max speed 50 km/h |
| Alt. Máx. 3.8m | Max height 3.8 m |
| Trânsito Proibido a Pesados | Heavy vehicles banned |
