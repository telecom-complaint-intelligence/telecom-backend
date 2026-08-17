--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4 (Debian 15.4-2.pgdg120+1)
-- Dumped by pg_dump version 15.4 (Debian 15.4-2.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: client_invitations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.client_invitations (
    id character varying(36) NOT NULL,
    email character varying(100) NOT NULL,
    department_id character varying(36) NOT NULL,
    token character varying(255) NOT NULL,
    is_activated boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    hashed_password character varying
);


ALTER TABLE public.client_invitations OWNER TO postgres;

--
-- Name: complaint_address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.complaint_address (
    id character varying(36) NOT NULL,
    complaint_id character varying(36) NOT NULL,
    address text,
    city character varying(100),
    state character varying(100),
    country character varying(100) NOT NULL,
    zipcode character varying(20)
);


ALTER TABLE public.complaint_address OWNER TO postgres;

--
-- Name: complaint_ai_analysis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.complaint_ai_analysis (
    id character varying(36) NOT NULL,
    complaint_id character varying(36) NOT NULL,
    category_confidence double precision,
    negativity_score double precision,
    sentiment_score double precision,
    component json,
    failure_type json,
    scope character varying(50),
    service_impact character varying(50),
    duration_hours double precision,
    occurrence_pattern character varying(50),
    extraction_source character varying(50),
    lowest_confidence double precision,
    created_at timestamp without time zone NOT NULL,
    solution_a text,
    solution_high text,
    warnings json,
    evidence json,
    confidence_score double precision,
    diagnosis character varying(255),
    root_cause text,
    risk_level character varying(50),
    policy_status character varying(50),
    final_decision character varying(100),
    critic_feedback text,
    reasoning text
);


ALTER TABLE public.complaint_ai_analysis OWNER TO postgres;

--
-- Name: complaint_priority_scores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.complaint_priority_scores (
    id character varying(36) NOT NULL,
    complaint_id character varying(36) NOT NULL,
    complexity character varying(50) NOT NULL,
    complexity_score integer NOT NULL,
    weighted_complexity_score double precision NOT NULL,
    weighted_negativity_score double precision NOT NULL,
    total_complexity_score double precision NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.complaint_priority_scores OWNER TO postgres;

--
-- Name: complaints; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.complaints (
    id character varying(36) NOT NULL,
    ticket_number character varying(50),
    user_id character varying(36),
    status character varying DEFAULT 'OPEN'::character varying NOT NULL,
    category character varying,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    complaint1 text NOT NULL,
    response text,
    complaint2 text,
    filling_on_behalf_of boolean DEFAULT false NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL,
    closing_time_stamp timestamp without time zone,
    customer_feedback boolean
);


ALTER TABLE public.complaints OWNER TO postgres;

--
-- Name: departments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departments (
    id character varying(36) NOT NULL,
    name character varying(100) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    is_archived boolean NOT NULL
);


ALTER TABLE public.departments OWNER TO postgres;

--
-- Name: profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profiles (
    id character varying(36) NOT NULL,
    user_id character varying(36) NOT NULL,
    name character varying,
    phone character varying,
    profile_picture character varying,
    address character varying,
    city character varying,
    state_val character varying,
    country character varying,
    zipcode character varying,
    is_complete boolean NOT NULL
);


ALTER TABLE public.profiles OWNER TO postgres;

--
-- Name: service_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.service_details (
    id character varying(36) NOT NULL,
    user_id character varying(36) NOT NULL,
    account_ref character varying,
    bill_cycle character varying,
    active_plan character varying,
    connection_status character varying,
    plan_usage character varying
);


ALTER TABLE public.service_details OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id character varying(36) NOT NULL,
    customer_id character varying(50),
    email character varying NOT NULL,
    hashed_password character varying,
    role character varying NOT NULL,
    email_verified boolean NOT NULL,
    cookie_consent boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    verification_otp character varying(6),
    otp_created_at timestamp without time zone,
    department_id character varying(36),
    is_archived boolean NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
98f40fd7dbf7
\.


--
-- Data for Name: client_invitations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.client_invitations (id, email, department_id, token, is_activated, created_at, expires_at, hashed_password) FROM stdin;
\.


--
-- Data for Name: complaint_address; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.complaint_address (id, complaint_id, address, city, state, country, zipcode) FROM stdin;
106cc18b-4114-4e06-a66a-a9827e5a5f4c	8cc41f1f-5880-4ad1-838b-bc6864e4947c	77 Sector B, Anna Nagar	Chennai	Tamil Nadu	India	600040
78ca273e-16aa-4578-b1e4-5406500ea057	35f8619e-85d1-46d1-b454-f7fc192edcdc	99 Cross Street, Gandhi Nagar	Coimbatore	Tamil Nadu	India	641001
57f36ae5-8a69-47ac-899b-4b9f7c95fb19	1099a105-c763-4ee8-b55d-2503fb6e69a5	77 Sector B, Anna Nagar	Chennai	Tamil Nadu	India	600040
d20f381a-4b50-4548-8b9e-eb812b7d164e	b9aad2b8-8503-4990-96fe-782051895efe	77 Sector B, Anna Nagar	Chennai	Tamil Nadu	India	600040
8055211a-1dc7-44d9-ac01-1e3941c5a350	b6cbafa5-bf20-4dd1-985a-b7faf18e972f	77 Sector B, Anna Nagar	Chennai	Tamil Nadu	India	600040
06bf9554-f1c6-4acc-95b2-4abf2aafe8fe	902b254a-7314-4030-b0e7-21c69bfc5fac	77 Sector B, Anna Nagar	Chennai	Tamil Nadu	India	600040
e925f7ed-04c7-4b1a-979b-384063094913	5ba1bdcc-f673-4c16-9013-7d95f47e7658	77 Sector B, Anna Nagar	Chennai	Tamil Nadu	India	600040
\.


--
-- Data for Name: complaint_ai_analysis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.complaint_ai_analysis (id, complaint_id, category_confidence, negativity_score, sentiment_score, component, failure_type, scope, service_impact, duration_hours, occurrence_pattern, extraction_source, lowest_confidence, created_at, solution_a, solution_high, warnings, evidence, confidence_score, diagnosis, root_cause, risk_level, policy_status, final_decision, critic_feedback, reasoning) FROM stdin;
0901200a-aada-46e6-b1b3-8899af49d182	a82112bb-5c3e-448e-8e3e-fc5ec11af844	0.977	0.8639	86.39	["fiber_cable"]	["physical_damage"]	multiple_users	complete_outage	\N	one_time	llm	0.304	2026-08-16 13:38:54.901563	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
0ef404a9-dcd6-48a8-9f88-90ef089b0bff	8b343e99-5625-4c96-b3e8-53ed3b67e36a	0.9741	0.9009	90.09	["fiber_cable"]	["cable_cut"]	area_wide	complete_outage	\N	one_time	llm	0.303	2026-08-16 13:38:56.861339	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
a76be725-429c-4459-a0f6-342991c26263	a1f9aa5b-2d3f-4b28-812b-87a4ae6330ed	0.9755	0.9131	91.31	["fiber_cable"]	["physical_damage"]	individual	complete_outage	\N	one_time	llm	0.262	2026-08-16 13:39:07.537983	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
d6f3abf4-8269-4c2c-9ef3-6ad9bc7a2fc8	4d525515-74fb-4e70-adf2-795bc7e4fe59	0.977	0.8639	86.39	["fiber_cable"]	["physical_damage"]	multiple_users	complete_outage	168	recurring	llm	0.304	2026-08-16 13:43:30.154921	Automated Triage: Inspect fiber_cable for physical_damage and verify service restoration.	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
57521ea1-d448-4007-8089-bde64f081be0	00db292f-939e-40b5-a327-c833e3e1ccd2	0.9741	0.9009	90.09	["fiber_cable"]	["cable_cut"]	area_wide	complete_outage	\N	one_time	llm	0.303	2026-08-16 13:43:33.116183	Automated Triage: Inspect fiber_cable for cable_cut and verify service restoration.	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
b7a0faa1-0850-45e9-9a6a-9671e990deb0	8cc41f1f-5880-4ad1-838b-bc6864e4947c	0.977	0.8639	86.39	["fiber_cable"]	["physical_damage"]	multiple_users	complete_outage	168	recurring	llm	0.304	2026-08-16 14:55:37.490777	Automated Triage: Inspect fiber_cable for physical_damage and verify service restoration.	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
d3479b4f-3dbc-4efb-8b3f-85f4eb4947bc	1c40318a-daf2-4813-a685-eef47723ea2d	0.7278	0.5171	51.71	["ont"]	["unknown"]	unknown	unknown	\N	unknown	llm	0.246	2026-08-16 14:55:41.490269	Automated Triage: Inspect ont for unknown and verify service restoration.	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
f0afa289-fc52-4a25-94eb-5343f32ad195	35f8619e-85d1-46d1-b454-f7fc192edcdc	0.8505	0.7509	75.09	["network_tower"]	["physical_damage"]	individual	complete_outage	\N	one_time	llm	0.176	2026-08-16 14:57:27.573608	Automated Triage: Inspect network_tower for physical_damage and verify service restoration.	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
d2d5cf23-e699-43bf-9074-39dcc55bf450	76208fd6-c640-48a3-b059-9c90ef4b4a87	0.8773	0.4449	44.49	["ont"]	["physical_damage"]	unknown	unknown	\N	one_time	llm	0.385	2026-08-16 14:57:30.264574	Automated Triage: Inspect ont for physical_damage and verify service restoration.	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
cad688f1-c495-4181-b210-355a5ccdb68a	1099a105-c763-4ee8-b55d-2503fb6e69a5	0.977	0.8639	86.39	["fiber_cable"]	["physical_damage"]	multiple_users	complete_outage	\N	one_time	llm	0.304	2026-08-16 15:04:31.727808	Automated Triage: Inspect fiber_cable for physical_damage and verify service restoration.	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
bd6e7a42-4918-48eb-919e-641fe7942693	f98d39fb-0d89-4e34-b782-b7b4710feec1	0.7278	0.5171	51.71	["ont"]	["physical_damage"]	unknown	unknown	\N	one_time	llm	0.246	2026-08-16 15:04:34.154822	Automated Triage: Inspect ont for physical_damage and verify service restoration.	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
9230a45a-f731-4974-9a10-be3d2f6d6078	b9aad2b8-8503-4990-96fe-782051895efe	0.977	0.8639	86.39	["unknown"]	["unknown"]	unknown	unknown	\N	unknown	llm	0.304	2026-08-16 18:44:50.088285	Automated Triage: Inspect unknown for unknown and verify service restoration.	\N	null	null	\N	\N	\N	\N	\N	\N	\N	Score breakdown -> scope(unknown)=2, impact(unknown)=2, component_max=2, failure_max=2, raw_total=12 | combined_raw=12 -> LOW (25/100)
f033e454-1721-4b00-99eb-826e68b3b506	48fcc2ec-205d-4fa4-a62d-83f4218b9c14	0.7278	0.5171	51.71	["unknown"]	["unknown"]	unknown	unknown	\N	unknown	llm	0.246	2026-08-16 18:44:51.038401	Automated Triage: Inspect unknown for unknown and verify service restoration.	\N	null	null	\N	\N	\N	\N	\N	\N	\N	Score breakdown -> scope(unknown)=2, impact(unknown)=2, component_max=2, failure_max=2, raw_total=12 | combined_raw=12 -> LOW (25/100)
b223e6ec-89ed-4d31-8b49-bf43f0f79a8f	b6cbafa5-bf20-4dd1-985a-b7faf18e972f	0.977	0.8639	86.39	["unknown"]	["unknown"]	unknown	unknown	\N	unknown	llm	0.304	2026-08-16 18:45:25.426662	Automated Triage: Inspect unknown for unknown and verify service restoration.	\N	null	null	\N	\N	\N	\N	\N	\N	\N	Score breakdown -> scope(unknown)=2, impact(unknown)=2, component_max=2, failure_max=2, raw_total=12 | combined_raw=12 -> LOW (25/100)
74dbf45a-c7ad-4827-84be-a6980a0a774a	873f7cb6-fb06-4125-a7fd-66e8316eb235	0.7278	0.5171	51.71	["unknown"]	["unknown"]	unknown	unknown	\N	unknown	llm	0.246	2026-08-16 18:45:26.40957	Automated Triage: Inspect unknown for unknown and verify service restoration.	\N	null	null	\N	\N	\N	\N	\N	\N	\N	Score breakdown -> scope(unknown)=2, impact(unknown)=2, component_max=2, failure_max=2, raw_total=12 | combined_raw=12 -> LOW (25/100)
34a445f5-966e-4736-b1f7-8f7f752b5dbf	aae40e45-4b76-4f8b-b9c9-190a82b26e4c	0.9577	0.8214	82.14	["unknown"]	["unknown"]	unknown	unknown	\N	unknown	llm	0.269	2026-08-16 18:45:27.425077	Automated Triage: Inspect unknown for unknown and verify service restoration.	\N	null	null	\N	\N	\N	\N	\N	\N	\N	Score breakdown -> scope(unknown)=2, impact(unknown)=2, component_max=2, failure_max=2, raw_total=12 | combined_raw=12 -> LOW (25/100)
8f9a764b-3aa3-466f-9104-19b18ad86557	4fdc8525-b252-4b43-8ac1-b238932c2bea	0.9476	0.5812	58.12	["unknown"]	["unknown"]	unknown	unknown	\N	unknown	llm	0.563	2026-08-16 18:45:28.36034	Automated Triage: Inspect unknown for unknown and verify service restoration.	Field engineering dispatched for on-site line quality and equipment inspection.	null	null	\N	Unresolved Customer Incident	Hardware or Line Signal Degradation	HIGH	ELEVATED	DISPATCH_FIELD_TECH	Customer feedback confirms standard self-care failure; technical on-site inspection recommended.	Customer indicated self-care steps did not resolve the issue. Escalated to Tier-2 technical support.
74fe0e58-ac58-4218-a84e-5fea83ef3091	902b254a-7314-4030-b0e7-21c69bfc5fac	0.977	0.8639	86.39	["unknown"]	["unknown"]	unknown	unknown	\N	unknown	llm	0.304	2026-08-16 18:49:11.768547	Automated Triage: Inspect unknown for unknown and verify service restoration.	\N	null	null	\N	\N	\N	\N	\N	\N	\N	Score breakdown -> scope(unknown)=2, impact(unknown)=2, component_max=2, failure_max=2, raw_total=12 | combined_raw=12 -> LOW (25/100)
ebccfa56-ed11-4434-83dc-a95cef34847f	58724c36-b62f-4527-9b26-a2fa242b351c	0.7278	0.5171	51.71	["unknown"]	["unknown"]	unknown	unknown	\N	unknown	llm	0.246	2026-08-16 18:49:12.730533	Automated Triage: Inspect unknown for unknown and verify service restoration.	\N	null	null	\N	\N	\N	\N	\N	\N	\N	Score breakdown -> scope(unknown)=2, impact(unknown)=2, component_max=2, failure_max=2, raw_total=12 | combined_raw=12 -> LOW (25/100)
368e8b0d-4890-4057-8eb4-d60c4154c76f	f1c2f806-75bb-4387-b151-bc32b0c09774	0.9577	0.8214	82.14	["unknown"]	["unknown"]	unknown	unknown	\N	unknown	llm	0.269	2026-08-16 18:49:13.987606	Automated Triage: Inspect unknown for unknown and verify service restoration.	\N	null	null	\N	\N	\N	\N	\N	\N	\N	Score breakdown -> scope(unknown)=2, impact(unknown)=2, component_max=2, failure_max=2, raw_total=12 | combined_raw=12 -> LOW (25/100)
d54dfa6b-13af-49fb-bd79-c83f733c9de7	40bb2c1c-3af2-46b4-a9be-0dd8c7179429	0.9476	0.5812	58.12	["unknown"]	["unknown"]	unknown	unknown	\N	unknown	llm	0.563	2026-08-16 18:49:15.317382	Automated Triage: Inspect unknown for unknown and verify service restoration.	Field engineering dispatched for on-site line quality and equipment inspection.	null	null	\N	Unresolved Customer Incident	Hardware or Line Signal Degradation	HIGH	ELEVATED	DISPATCH_FIELD_TECH	Customer feedback confirms standard self-care failure; technical on-site inspection recommended.	Customer indicated self-care steps did not resolve the issue. Escalated to Tier-2 technical support.
23d0e20a-7bed-42cf-b1f8-04c26ae7af45	5ba1bdcc-f673-4c16-9013-7d95f47e7658	0.977	0.8639	86.39	["fiber_cable"]	["physical_damage"]	multiple_users	complete_outage	168	recurring	llm	0.304	2026-08-16 18:50:17.009186	Escalate the complaint for further investigation and line inspection.	Escalate the complaint for further investigation and line inspection.	[]	[]	0.95	Internet Disconnection	UNKNOWN	HIGH	ELEVATED	ESCALATE	Proposal is conservative, matches HIGH risk for extended outage, and provides a clear operational action.	Score breakdown -> scope(multiple_users)=3, impact(complete_outage)=4, component_max=2, failure_max=4, raw_total=20 | Long unresolved duration: 168.0 hours | combined_raw=27 -> CRITICAL (88/100)
875ee3ed-a311-4705-ad8a-335fc11e4eae	973a0ecf-781c-490f-b803-e9c2bbe9f889	0.7278	0.5171	51.71	["ont"]	["physical_damage"]	unknown	unknown	\N	one_time	llm	0.246	2026-08-16 18:50:22.328655	1. Power cycle your router by disconnecting the power cable for 30 seconds, then plug it back in.\n2. Check that the WAN / PON indicator light on the router is steady green.\n3. Ensure your device is within 15 feet of the router without thick wall obstructions.	\N	["Do not press the factory reset pinhole button."]	[{"knowledge_id": "KB002", "title": "Intermittent Wi-Fi Disconnection"}, {"knowledge_id": "KB003", "title": "No Mobile Data"}, {"knowledge_id": "KB005", "title": "Slow Internet Diagnosis (Internal)"}]	0.9	\N	\N	\N	\N	\N	\N	Score breakdown -> scope(unknown)=2, impact(unknown)=2, component_max=1, failure_max=4, raw_total=13 | combined_raw=13 -> LOW (29/100)
fb528b38-47f8-46b9-b968-f8de940ea3dc	2c94bb82-c30a-4839-89aa-eab3b53cde29	0.9577	0.8214	82.14	["unknown"]	["unknown"]	unknown	unknown	\N	unknown	llm	0.269	2026-08-16 18:50:27.499238	1. Power cycle your router by disconnecting the power cable for 30 seconds, then plug it back in.\n2. Check that the WAN / PON indicator light on the router is steady green.\n3. Ensure your device is within 15 feet of the router without thick wall obstructions.	\N	["Do not press the factory reset pinhole button."]	[{"knowledge_id": "KB005", "title": "Slow Internet Diagnosis (Internal)"}, {"knowledge_id": "KB007", "title": "VoLTE Call Drops"}, {"knowledge_id": "KB001", "title": "Basic Router Troubleshooting"}]	0.9	\N	\N	\N	\N	\N	\N	Score breakdown -> scope(unknown)=2, impact(unknown)=2, component_max=2, failure_max=2, raw_total=12 | combined_raw=12 -> LOW (25/100)
90f294b1-db6d-4352-a76a-d6b9c74e9c07	cb417bbd-1d80-49c4-83b5-925dca8ca0a3	0.9476	0.5812	58.12	["unknown"]	["unknown"]	unknown	unknown	\N	unknown	llm	0.563	2026-08-16 18:50:32.145581	1. Power cycle your router by disconnecting the power cable for 30 seconds, then plug it back in.\n2. Check that the WAN / PON indicator light on the router is steady green.\n3. Ensure your device is within 15 feet of the router without thick wall obstructions.	Escalate the complaint for further investigation and line inspection.	["Do not press the factory reset pinhole button."]	[{"knowledge_id": "KB005", "title": "Slow Internet Diagnosis (Internal)"}, {"knowledge_id": "KB001", "title": "Basic Router Troubleshooting"}, {"knowledge_id": "KB002", "title": "Intermittent Wi-Fi Disconnection"}]	0.9	Internet Disconnection	UNKNOWN	HIGH	ELEVATED	ESCALATE	Proposal is conservative, matches HIGH risk for extended outage, and provides a clear operational action.	[Policy Decision: MEDIUM] escalated=True. Escalated to MEDIUM: Complaint is unresolved or the solution was irrelevant. LLM Insights: Decision policy analysis: Customer feedback=false, Resolution=unresolved.
ebce0c9b-7f06-4611-be02-6904e7e6f9bd	dd42c5f0-cff0-413d-ada0-ee44fca1d6ea	0.9642	0.6235	62.35	["router"]	["intermittent_connection"]	individual	degraded	24	one_time	llm	0.398	2026-08-16 18:56:01.887305	1. Power cycle your router by disconnecting the power cable for 30 seconds, then plug it back in.\n2. Check that the WAN / PON indicator light on the router is steady green.\n3. Ensure your device is within 15 feet of the router without thick wall obstructions.	\N	["Do not press the factory reset pinhole button."]	[{"knowledge_id": "KB001", "title": "Basic Router Troubleshooting"}, {"knowledge_id": "KB002", "title": "Intermittent Wi-Fi Disconnection"}, {"knowledge_id": "KB003", "title": "No Mobile Data"}]	0.9	\N	\N	\N	\N	\N	\N	Score breakdown -> scope(individual)=1, impact(degraded)=2, component_max=1, failure_max=1, raw_total=8 | combined_raw=8 -> LOW (8/100)
c92ad4c3-7689-4da4-afcd-f0643029a5b2	017de277-00f7-442c-963f-d25bde3d3c8d	0.9253	0.6613	66.13	["router"]	["intermittent_connection"]	individual	degraded	24	one_time	llm	0.224	2026-08-16 18:56:08.545951	1. Power cycle your router by disconnecting the power cable for 30 seconds, then plug it back in.\n2. Check that the WAN / PON indicator light on the router is steady green.\n3. Ensure your device is within 15 feet of the router without thick wall obstructions.	\N	["Do not press the factory reset pinhole button."]	[{"knowledge_id": "KB002", "title": "Intermittent Wi-Fi Disconnection"}, {"knowledge_id": "KB006", "title": "Repeated Router Restarts Failed"}, {"knowledge_id": "KB001", "title": "Basic Router Troubleshooting"}]	0.9	\N	\N	\N	\N	\N	\N	Score breakdown -> scope(individual)=1, impact(degraded)=2, component_max=1, failure_max=1, raw_total=8 | combined_raw=8 -> LOW (8/100)
3d8ee0fd-8962-4488-b5b9-b9d90ff4a66f	c2e2ea58-75fe-4a7a-84a1-863c0bfa5467	0.9693	0.832	83.2	["fiber_cable"]	["physical_damage"]	individual	complete_outage	168	one_time	llm	0.179	2026-08-16 18:56:09.596176	Escalate the complaint for further investigation and line inspection.	Escalate the complaint for further investigation and line inspection.	[]	[]	0.95	Internet Disconnection	UNKNOWN	HIGH	ELEVATED	ESCALATE	Proposal is conservative, matches HIGH risk for extended outage, and provides a clear operational action.	Score breakdown -> scope(individual)=1, impact(complete_outage)=4, component_max=2, failure_max=4, raw_total=16 | Long unresolved duration: 168.0 hours | combined_raw=23 -> CRITICAL (71/100)
7028e980-d04c-4afd-a09c-012f1c63dd53	1811186a-65be-459c-8208-718a698757c3	0.9494	0.7597	75.97	["fiber_cable"]	["cable_cut"]	area_wide	complete_outage	\N	one_time	llm	0.251	2026-08-16 18:56:12.702043	Escalate the complaint for further investigation and line inspection.	Escalate the complaint for further investigation and line inspection.	[]	[]	0.95	Internet Disconnection	UNKNOWN	HIGH	ELEVATED	ESCALATE	Proposal is conservative, matches HIGH risk for extended outage, and provides a clear operational action.	Large-scale (area_wide) complete outage involving critical infrastructure and/or a severe failure type
98674a6c-4945-4e33-84e6-4fc44f41405c	935aa0b9-096d-4e8f-ba81-0a9d6b1315f7	0.9724	0.6861	68.61	["unknown"]	["physical_damage"]	individual	degraded	\N	continuous	llm	0.389	2026-08-16 18:56:20.492047	Check the physical condition of the fiber optic cable and connectors\nEnsure the fiber optic connectors are securely attached\nRestart the router by switching it off, waiting 30 seconds, and then switching it back on	Escalate the complaint for further investigation and line inspection.	[]	[{"knowledge_id": "KB001", "title": "Basic Router Troubleshooting"}, {"knowledge_id": "KB002", "title": "Intermittent Wi-Fi Disconnection"}, {"knowledge_id": "KB003", "title": "No Mobile Data"}]	0.8	Internet Disconnection	UNKNOWN	HIGH	ELEVATED	ESCALATE	Proposal is conservative, matches HIGH risk for extended outage, and provides a clear operational action.	[Policy Decision: HIGH] escalated=True. Escalated to HIGH: Complaint remains unresolved or the solution was irrelevant. LLM Insights: Decision policy analysis: Customer feedback=false, Resolution=unresolved.
\.


--
-- Data for Name: complaint_priority_scores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.complaint_priority_scores (id, complaint_id, complexity, complexity_score, weighted_complexity_score, weighted_negativity_score, total_complexity_score, created_at) FROM stdin;
928c923a-08ea-4818-a9bd-398439c9d159	a82112bb-5c3e-448e-8e3e-fc5ec11af844	MEDIUM	58	49.3	12.9585	62.2585	2026-08-16 13:38:54.906489
b8f2200d-bf20-47dd-9ea4-1da84dff6d19	8b343e99-5625-4c96-b3e8-53ed3b67e36a	CRITICAL	100	85	13.5135	98.5135	2026-08-16 13:38:56.862996
aaaccf37-efbc-4ce4-9de8-29a3d10986f5	a1f9aa5b-2d3f-4b28-812b-87a4ae6330ed	MEDIUM	42	35.7	13.6965	49.3965	2026-08-16 13:39:07.540353
1eabf886-1d09-4ed6-a283-d6229ae2bf64	4d525515-74fb-4e70-adf2-795bc7e4fe59	CRITICAL	88	74.8	12.9585	87.7585	2026-08-16 13:43:30.156554
8571c547-800a-4dcd-859c-f92691cb890a	00db292f-939e-40b5-a327-c833e3e1ccd2	CRITICAL	100	85	13.5135	98.5135	2026-08-16 13:43:33.117696
c5261f24-7e1e-4807-83c1-01a200e192d8	8cc41f1f-5880-4ad1-838b-bc6864e4947c	CRITICAL	88	74.8	12.9585	87.7585	2026-08-16 14:55:37.495813
54be1089-8b4a-4093-b08f-16ef935185f5	1c40318a-daf2-4813-a685-eef47723ea2d	LOW	21	17.85	7.7565	25.6065	2026-08-16 14:55:41.49257
8a9903d1-b2ce-4de4-b08e-96b801872778	35f8619e-85d1-46d1-b454-f7fc192edcdc	CRITICAL	100	85	11.2635	96.2635	2026-08-16 14:57:27.57603
50427d30-7036-4575-8445-02d527bfef02	76208fd6-c640-48a3-b059-9c90ef4b4a87	LOW	29	24.65	6.6735	31.3235	2026-08-16 14:57:30.265565
a8cbfbd7-24f2-4db8-a46d-4e9e0e4c3a37	1099a105-c763-4ee8-b55d-2503fb6e69a5	MEDIUM	58	49.3	12.9585	62.2585	2026-08-16 15:04:31.730906
aa9988ab-3742-490a-be66-5b9268b9b76f	f98d39fb-0d89-4e34-b782-b7b4710feec1	LOW	29	24.65	7.7565	32.4065	2026-08-16 15:04:34.156099
5bbe1faf-be6a-4956-8303-a6c7b5533997	b9aad2b8-8503-4990-96fe-782051895efe	LOW	25	21.25	12.9585	34.2085	2026-08-16 18:44:50.090687
ba842427-21bf-48d1-a106-34b084de2e0e	48fcc2ec-205d-4fa4-a62d-83f4218b9c14	LOW	25	21.25	7.7565	29.0065	2026-08-16 18:44:51.040298
396c83e0-e40f-469b-b1fe-4f6b2813d67a	b6cbafa5-bf20-4dd1-985a-b7faf18e972f	LOW	25	21.25	12.9585	34.2085	2026-08-16 18:45:25.439935
2ce3d642-0555-4dfa-bcba-36aa219a307e	873f7cb6-fb06-4125-a7fd-66e8316eb235	LOW	25	21.25	7.7565	29.0065	2026-08-16 18:45:26.411458
6f2f68f5-035a-4df1-b032-1fe7feadeace	aae40e45-4b76-4f8b-b9c9-190a82b26e4c	LOW	25	21.25	12.321	33.571	2026-08-16 18:45:27.426177
f9b05579-7c68-47a8-87f5-97f54345c2cf	4fdc8525-b252-4b43-8ac1-b238932c2bea	LOW	25	21.25	8.718	29.968	2026-08-16 18:45:28.362048
388fd652-5957-4f73-9c63-a1fa6faf822f	902b254a-7314-4030-b0e7-21c69bfc5fac	LOW	25	21.25	12.9585	34.2085	2026-08-16 18:49:11.772187
2e7bed7f-ebf9-4d7e-b23a-b456c2b948f7	58724c36-b62f-4527-9b26-a2fa242b351c	LOW	25	21.25	7.7565	29.0065	2026-08-16 18:49:12.731859
21b9e75c-ba77-4887-8fe6-b0c4dfbd48d0	f1c2f806-75bb-4387-b151-bc32b0c09774	LOW	25	21.25	12.321	33.571	2026-08-16 18:49:13.988969
dd4a5abc-1107-4867-89c1-9880040d591c	40bb2c1c-3af2-46b4-a9be-0dd8c7179429	LOW	25	21.25	8.718	29.968	2026-08-16 18:49:15.318279
43c09bd7-aa2b-4c7a-9112-9ef610418353	5ba1bdcc-f673-4c16-9013-7d95f47e7658	CRITICAL	88	74.8	12.9585	87.7585	2026-08-16 18:50:17.013269
a8d2c26e-655d-4ba2-a9ea-60b05aab4342	973a0ecf-781c-490f-b803-e9c2bbe9f889	LOW	29	24.65	7.7565	32.4065	2026-08-16 18:50:22.330412
f07870a3-bdc8-4649-b5fd-64a2d9016b56	2c94bb82-c30a-4839-89aa-eab3b53cde29	LOW	25	21.25	12.321	33.571	2026-08-16 18:50:27.500187
95f80c4e-4193-44e2-8cb9-3703f7f3ac25	cb417bbd-1d80-49c4-83b5-925dca8ca0a3	LOW	25	21.25	8.718	29.968	2026-08-16 18:50:32.146637
56daa463-6b07-4523-b9be-f5d34574e5b8	dd42c5f0-cff0-413d-ada0-ee44fca1d6ea	LOW	8	6.8	9.3525	16.1525	2026-08-16 18:56:01.889174
f590b0fc-8f7e-4eb5-bced-12b79115f6d8	017de277-00f7-442c-963f-d25bde3d3c8d	LOW	8	6.8	9.9195	16.7195	2026-08-16 18:56:08.547549
d011db13-2319-4786-ad57-bd13f6750444	c2e2ea58-75fe-4a7a-84a1-863c0bfa5467	CRITICAL	71	60.35	12.48	72.83	2026-08-16 18:56:09.597018
f9da7230-f19e-4bfa-8bc3-b2af51c74ddb	1811186a-65be-459c-8208-718a698757c3	CRITICAL	100	85	11.3955	96.3955	2026-08-16 18:56:12.702766
d8d3bc29-e5ab-4ea5-9077-e24d46ad9d84	935aa0b9-096d-4e8f-ba81-0a9d6b1315f7	MEDIUM	54	45.9	10.2915	56.1915	2026-08-16 18:56:20.494191
\.


--
-- Data for Name: complaints; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.complaints (id, ticket_number, user_id, status, category, created_at, complaint1, response, complaint2, filling_on_behalf_of, "timestamp", closing_time_stamp, customer_feedback) FROM stdin;
d6d98f5d-a5a3-417a-932e-38ea44db6b69	\N	\N	OPEN	Internet / Connectivity	2026-08-16 04:56:21.924278	the network tower near my house got bursted	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
61eec230-7679-41fa-8295-451028869d3c	\N	\N	OPEN	Internet / Connectivity	2026-08-16 06:09:50.419977	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
11aae52c-5e4f-4723-ba25-3cf641b1bd92	\N	\N	OPEN	Internet / Connectivity	2026-08-16 07:40:49.77282	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
ef3079b1-c1c3-493f-8de8-46e6b01c7acf	34560	\N	OPEN	Internet / Connectivity	2026-08-16 07:45:57.228498	the network tower near my house is blasted	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
3cc61786-013c-45d0-a127-d3a3492b4616	\N	\N	OPEN	Internet / Connectivity	2026-08-16 07:47:36.076895	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
ae879036-f758-4590-bfd1-f8b39670eb6a	\N	\N	OPEN	Internet / Connectivity	2026-08-16 07:51:18.035423	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
ebe492b7-4522-4c41-b7db-9bd70d005265	\N	\N	OPEN	Internet / Connectivity	2026-08-16 09:51:05.219623	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
a41f85c2-bd91-4484-b497-e75c7e48c66a	TICK-691942	\N	OPEN	Internet / Connectivity	2026-08-16 11:20:55.722597	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
08f99ac2-5e61-41db-a5ef-9e99d393f681	TICK-407905	319d3ab4-86f9-40f1-b135-3b5739c2ee96	OPEN	Internet / Connectivity	2026-08-16 11:21:01.133643	Complete outage in my neighborhood, fiber cable is cut down.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
2e8394a8-bb0c-4938-a874-4e30aa971b56	TICK-369527	7ff0b7c4-6ddd-4e10-bd38-e0508a46897d	OPEN	Internet / Connectivity	2026-08-16 11:21:26.881904	the internet fiber cable near my street is damaged and completely broken	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
07440fba-b7fb-4837-be0a-62f86aee7518	string	\N	OPEN	Internet / Connectivity	2026-08-16 11:27:29.349302	string	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
cf7a1bbb-593b-40c8-8d62-1320ce919dec	TICK-787364	\N	OPEN	Internet / Connectivity	2026-08-16 11:29:33.070264	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
af7ff081-d375-4622-a747-4213d3d28c7c	TICK-186902	010e777c-ab8a-4c1b-9383-5add4f2089a4	OPEN	Internet / Connectivity	2026-08-16 11:29:35.730273	Complete outage in my neighborhood, fiber cable is cut down.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
baa7616a-a544-4490-8b1a-5d8c107c19a0	TICK-244665	\N	OPEN	Internet / Connectivity	2026-08-16 13:07:54.800543	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
5a3bf9a9-cfe9-4a14-9e90-a5edb5c64402	TICK-694128	6f98f616-647b-4736-b53c-415da8a8cf53	OPEN	Internet / Connectivity	2026-08-16 13:07:57.586573	Complete outage in my neighborhood, fiber cable is cut down.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
a82112bb-5c3e-448e-8e3e-fc5ec11af844	TICK-510761	\N	OPEN	Internet / Connectivity	2026-08-16 13:38:54.896604	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
8b343e99-5625-4c96-b3e8-53ed3b67e36a	TICK-756471	e540822c-f948-4a01-b102-5b55c2f29c01	OPEN	Internet / Connectivity	2026-08-16 13:38:56.85881	Complete outage in my neighborhood, fiber cable is cut down.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
a1f9aa5b-2d3f-4b28-812b-87a4ae6330ed	TICK-169868	\N	OPEN	Internet / Connectivity	2026-08-16 13:39:07.533369	the internet fiber cable near my street is damaged and completely broken	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
4d525515-74fb-4e70-adf2-795bc7e4fe59	TICK-489823	\N	OPEN	Internet / Connectivity	2026-08-16 13:43:30.151183	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
00db292f-939e-40b5-a327-c833e3e1ccd2	TICK-733556	43981d24-5839-4071-a69d-63beaa18832a	OPEN	Internet / Connectivity	2026-08-16 13:43:33.113627	Complete outage in my neighborhood, fiber cable is cut down.	\N	\N	f	2026-08-16 14:51:12.62857	\N	\N
8cc41f1f-5880-4ad1-838b-bc6864e4947c	TICK-643826	\N	OPEN	Internet / Connectivity	2026-08-16 14:55:37.485642	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	Automated Triage: Inspect fiber_cable for physical_damage and verify service restoration.	\N	t	2026-08-16 14:55:37.485638	\N	\N
1c40318a-daf2-4813-a685-eef47723ea2d	TICK-503109	8fc93110-4a04-40d1-94c4-ff9da1b59353	RESOLVED	Internet / Connectivity	2026-08-16 14:55:41.485267	Broadband optical signal is red on my ONT router.	Automated Triage: Inspect ont for unknown and verify service restoration.	Technician visited and spliced the fiber, light is now green.	f	2026-08-16 14:55:41.485264	2026-08-16 14:55:41.532959	\N
35f8619e-85d1-46d1-b454-f7fc192edcdc	TICK-426042	7ff0b7c4-6ddd-4e10-bd38-e0508a46897d	OPEN	Internet / Connectivity	2026-08-16 14:57:27.570336	Tower battery exploded in my uncle shop building	Automated Triage: Inspect network_tower for physical_damage and verify service restoration.	\N	t	2026-08-16 14:57:27.570333	\N	\N
76208fd6-c640-48a3-b059-9c90ef4b4a87	TICK-556930	7ff0b7c4-6ddd-4e10-bd38-e0508a46897d	RESOLVED	Internet / Connectivity	2026-08-16 14:57:30.262878	ONT optical LOS blinking red in my own house	Automated Triage: Inspect ont for physical_damage and verify service restoration.	Technician replaced fiber patch cable, internet working now.	f	2026-08-16 14:57:30.262874	2026-08-16 14:57:30.28227	\N
1099a105-c763-4ee8-b55d-2503fb6e69a5	TICK-576026	\N	OPEN	Internet / Connectivity	2026-08-16 15:04:31.723422	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	Automated Triage: Inspect fiber_cable for physical_damage and verify service restoration.	\N	t	2026-08-16 15:04:31.723419	\N	\N
f98d39fb-0d89-4e34-b782-b7b4710feec1	TICK-822402	802000c3-595a-4b4b-b853-50b4552a7f9c	RESOLVED	Internet / Connectivity	2026-08-16 15:04:34.151159	Broadband optical signal is red on my ONT router.	Automated Triage: Inspect ont for physical_damage and verify service restoration.	Technician visited and spliced the fiber, light is now green.	f	2026-08-16 15:04:34.151158	2026-08-16 15:04:34.172816	\N
b9aad2b8-8503-4990-96fe-782051895efe	TICK-964418	\N	OPEN	Internet / Connectivity	2026-08-16 18:44:50.08243	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	Automated Triage: Inspect unknown for unknown and verify service restoration.	\N	t	2026-08-16 18:44:50.082427	\N	\N
48fcc2ec-205d-4fa4-a62d-83f4218b9c14	TICK-455818	18ff6235-911a-473a-860c-e0bcdf972582	RESOLVED	Internet / Connectivity	2026-08-16 18:44:51.035586	Broadband optical signal is red on my ONT router.	Automated Triage: Inspect unknown for unknown and verify service restoration.	Technician visited and spliced the fiber, light is now green.	f	2026-08-16 18:44:51.035584	2026-08-16 18:44:51.058173	\N
b6cbafa5-bf20-4dd1-985a-b7faf18e972f	TICK-984909	\N	OPEN	Internet / Connectivity	2026-08-16 18:45:25.419104	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	Automated Triage: Inspect unknown for unknown and verify service restoration.	\N	t	2026-08-16 18:45:25.4191	\N	\N
873f7cb6-fb06-4125-a7fd-66e8316eb235	TICK-772359	5c531f9d-c62a-406f-8e63-1e376d830e62	RESOLVED	Internet / Connectivity	2026-08-16 18:45:26.397951	Broadband optical signal is red on my ONT router.	Automated Triage: Inspect unknown for unknown and verify service restoration.	Technician visited and spliced the fiber, light is now green.	f	2026-08-16 18:45:26.397947	2026-08-16 18:45:26.438842	\N
aae40e45-4b76-4f8b-b9c9-190a82b26e4c	TICK-524720	\N	RESOLVED	Internet / Connectivity	2026-08-16 18:45:27.423894	My wifi connection drops intermittently	Automated Triage: Inspect unknown for unknown and verify service restoration.	\N	f	2026-08-16 18:45:27.423891	2026-08-16 18:45:27.439595	t
4fdc8525-b252-4b43-8ac1-b238932c2bea	TICK-369280	\N	ESCALATED	Internet / Connectivity	2026-08-16 18:45:28.357293	Optical loss error LOS light blinking red continuously	Field engineering dispatched for on-site line quality and equipment inspection.	\N	f	2026-08-16 18:45:28.357274	\N	f
902b254a-7314-4030-b0e7-21c69bfc5fac	TICK-619199	\N	OPEN	Internet / Connectivity	2026-08-16 18:49:11.763693	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	Automated Triage: Inspect unknown for unknown and verify service restoration.	\N	t	2026-08-16 18:49:11.76369	\N	\N
58724c36-b62f-4527-9b26-a2fa242b351c	TICK-803976	ebd95344-744e-44dc-8f0b-d8c442a641aa	RESOLVED	Internet / Connectivity	2026-08-16 18:49:12.728747	Broadband optical signal is red on my ONT router.	Automated Triage: Inspect unknown for unknown and verify service restoration.	Technician visited and spliced the fiber, light is now green.	f	2026-08-16 18:49:12.728745	2026-08-16 18:49:12.751765	\N
f1c2f806-75bb-4387-b151-bc32b0c09774	TICK-298154	\N	RESOLVED	Internet / Connectivity	2026-08-16 18:49:13.985139	My wifi connection drops intermittently	Automated Triage: Inspect unknown for unknown and verify service restoration.	\N	f	2026-08-16 18:49:13.985135	2026-08-16 18:49:14.010373	t
40bb2c1c-3af2-46b4-a9be-0dd8c7179429	TICK-656485	\N	ESCALATED	Internet / Connectivity	2026-08-16 18:49:15.315088	Optical loss error LOS light blinking red continuously	Field engineering dispatched for on-site line quality and equipment inspection.	\N	f	2026-08-16 18:49:15.315083	\N	f
5ba1bdcc-f673-4c16-9013-7d95f47e7658	TICK-180789	\N	OPEN	Internet / Connectivity	2026-08-16 18:50:17.003569	Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.	Escalate the complaint for further investigation and line inspection.	\N	t	2026-08-16 18:50:17.00356	\N	\N
973a0ecf-781c-490f-b803-e9c2bbe9f889	TICK-897451	57c98237-c797-42e5-8a6d-867e51fe7c3d	RESOLVED	Internet / Connectivity	2026-08-16 18:50:22.320939	Broadband optical signal is red on my ONT router.	1. Power cycle your router by disconnecting the power cable for 30 seconds, then plug it back in.\n2. Check that the WAN / PON indicator light on the router is steady green.\n3. Ensure your device is within 15 feet of the router without thick wall obstructions.	Technician visited and spliced the fiber, light is now green.	f	2026-08-16 18:50:22.320927	2026-08-16 18:50:22.364967	\N
2c94bb82-c30a-4839-89aa-eab3b53cde29	TICK-741785	\N	RESOLVED	Internet / Connectivity	2026-08-16 18:50:27.497574	My wifi connection drops intermittently	1. Power cycle your router by disconnecting the power cable for 30 seconds, then plug it back in.\n2. Check that the WAN / PON indicator light on the router is steady green.\n3. Ensure your device is within 15 feet of the router without thick wall obstructions.	\N	f	2026-08-16 18:50:27.49757	2026-08-16 18:50:27.517407	t
cb417bbd-1d80-49c4-83b5-925dca8ca0a3	TICK-138759	\N	ESCALATED	Internet / Connectivity	2026-08-16 18:50:32.143613	Optical loss error LOS light blinking red continuously	Escalate the complaint for further investigation and line inspection.	\N	f	2026-08-16 18:50:32.143594	\N	f
dd42c5f0-cff0-413d-ada0-ee44fca1d6ea	TICK-333357	\N	OPEN	Internet / Connectivity	2026-08-16 18:56:01.882063	My wifi connection is dropping occasionally on phone	1. Power cycle your router by disconnecting the power cable for 30 seconds, then plug it back in.\n2. Check that the WAN / PON indicator light on the router is steady green.\n3. Ensure your device is within 15 feet of the router without thick wall obstructions.	\N	f	2026-08-16 18:56:01.882057	\N	\N
017de277-00f7-442c-963f-d25bde3d3c8d	TICK-269901	\N	OPEN	Internet / Connectivity	2026-08-16 18:56:08.543922	Broadband optical ONT router has intermittent sync failure	1. Power cycle your router by disconnecting the power cable for 30 seconds, then plug it back in.\n2. Check that the WAN / PON indicator light on the router is steady green.\n3. Ensure your device is within 15 feet of the router without thick wall obstructions.	\N	f	2026-08-16 18:56:08.54391	\N	\N
c2e2ea58-75fe-4a7a-84a1-863c0bfa5467	TICK-106550	\N	OPEN	Internet / Connectivity	2026-08-16 18:56:09.594805	Apartment main fiber junction box damaged and offline for 96 hours	Escalate the complaint for further investigation and line inspection.	\N	f	2026-08-16 18:56:09.594803	\N	\N
1811186a-65be-459c-8208-718a698757c3	TICK-774006	\N	OPEN	Internet / Connectivity	2026-08-16 18:56:12.700923	Critical fiber optic cable cut on main street, emergency hospital and thousands offline	Escalate the complaint for further investigation and line inspection.	\N	f	2026-08-16 18:56:12.700922	\N	\N
935aa0b9-096d-4e8f-ba81-0a9d6b1315f7	TICK-481333	\N	ESCALATED	Equipment / Router	2026-08-16 18:56:20.490198	LOS red light on fiber router is blinking constantly	Escalate the complaint for further investigation and line inspection.	\N	f	2026-08-16 18:56:20.490195	\N	f
\.


--
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.departments (id, name, created_at, is_archived) FROM stdin;
\.


--
-- Data for Name: profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.profiles (id, user_id, name, phone, profile_picture, address, city, state_val, country, zipcode, is_complete) FROM stdin;
d1c7dc2d-a47d-491e-9dbb-7a3e10b7efcd	319d3ab4-86f9-40f1-b135-3b5739c2ee96	John Doe	9876543210	\N	\N	Atlanta	Georgia	\N	30301	t
795eadbf-ff3b-4725-bf90-b4bc4578773d	7ff0b7c4-6ddd-4e10-bd38-e0508a46897d	Arun Kumar	9876543210	\N	42 Anna Salai	Chennai	Tamil Nadu	India	600078	t
b4d893ad-9001-4c53-98e7-14ddc98d216b	010e777c-ab8a-4c1b-9383-5add4f2089a4	John Doe	9876543210	\N	\N	Atlanta	Georgia	\N	30301	t
8ec66339-d103-4440-abee-0346f59ce613	6f98f616-647b-4736-b53c-415da8a8cf53	John Doe	9876543210	\N	\N	Atlanta	Georgia	\N	30301	t
32b0b85a-4d9e-45ad-8472-fb6630b189d2	e540822c-f948-4a01-b102-5b55c2f29c01	John Doe	9876543210	\N	\N	Atlanta	Georgia	\N	30301	t
67fc87d8-1c47-4def-aab2-5dcfcf8c1239	43981d24-5839-4071-a69d-63beaa18832a	John Doe	9876543210	\N	\N	Atlanta	Georgia	\N	30301	t
b038be25-6dbc-4c33-a8d0-64dd82a63d5c	08fb8a17-dc07-4b14-bcf4-b4cf18ff61e5	Priya Sharma	9876543210	\N	10 Marina Beach Rd	Chennai	Tamil Nadu	India	600001	t
fe094396-72a9-4c55-9ac4-6554c6eb8494	8fc93110-4a04-40d1-94c4-ff9da1b59353	Priya Sharma	9876543210	\N	10 Marina Beach Rd	Chennai	Tamil Nadu	India	600001	t
a39bf124-f30a-4d9b-a083-f7c6257492d1	802000c3-595a-4b4b-b853-50b4552a7f9c	Priya Sharma	9876543210	\N	10 Marina Beach Rd	Chennai	Tamil Nadu	India	600001	t
aa98e600-744c-453e-880d-ec12ba6d8050	18ff6235-911a-473a-860c-e0bcdf972582	Priya Sharma	9876543210	\N	10 Marina Beach Rd	Chennai	Tamil Nadu	India	600001	t
df253e33-445d-4280-a215-499cbe84db86	5c531f9d-c62a-406f-8e63-1e376d830e62	Priya Sharma	9876543210	\N	10 Marina Beach Rd	Chennai	Tamil Nadu	India	600001	t
0f5a9b68-e1ef-48ce-a8f3-bb310cd71b5d	ebd95344-744e-44dc-8f0b-d8c442a641aa	Priya Sharma	9876543210	\N	10 Marina Beach Rd	Chennai	Tamil Nadu	India	600001	t
c28ab750-2b99-46e2-986b-19592b5a8390	57c98237-c797-42e5-8a6d-867e51fe7c3d	Priya Sharma	9876543210	\N	10 Marina Beach Rd	Chennai	Tamil Nadu	India	600001	t
\.


--
-- Data for Name: service_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.service_details (id, user_id, account_ref, bill_cycle, active_plan, connection_status, plan_usage) FROM stdin;
616b7c15-f7b1-4d1d-bc2e-3429a3a45243	7ff0b7c4-6ddd-4e10-bd38-e0508a46897d	\N	\N	\N	\N	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, customer_id, email, hashed_password, role, email_verified, cookie_consent, created_at, verification_otp, otp_created_at, department_id, is_archived) FROM stdin;
319d3ab4-86f9-40f1-b135-3b5739c2ee96	CUST-CA417368	testuser_4713d4@example.com	\N	customer	t	f	2026-08-16 11:20:55.736853	\N	\N	\N	f
7ff0b7c4-6ddd-4e10-bd38-e0508a46897d	CUST-OTRNR814	telu_user_99@gmail.com	$2b$12$ivzuzUGo7.cZRZgYHGAVfOJtZB11GbwvPb2ba2uh8GHeE9f6BuGU2	customer	f	f	2026-08-16 11:21:23.929596	512517	2026-08-16 11:21:23.928813	\N	f
010e777c-ab8a-4c1b-9383-5add4f2089a4	CUST-F9185F72	testuser_bf205b@example.com	\N	customer	t	f	2026-08-16 11:29:33.080008	\N	\N	\N	f
6f98f616-647b-4736-b53c-415da8a8cf53	CUST-DB049547	testuser_a03ca3@example.com	\N	customer	t	f	2026-08-16 13:07:54.820592	\N	\N	\N	f
e540822c-f948-4a01-b102-5b55c2f29c01	CUST-834867F1	testuser_046382@example.com	\N	customer	t	f	2026-08-16 13:38:54.922798	\N	\N	\N	f
43981d24-5839-4071-a69d-63beaa18832a	CUST-7790A44E	testuser_2a99e6@example.com	\N	customer	t	f	2026-08-16 13:43:30.169335	\N	\N	\N	f
08fb8a17-dc07-4b14-bcf4-b4cf18ff61e5	CUST-BB0B20ED	testuser_1bd4c6@example.com	\N	customer	t	f	2026-08-16 14:53:38.761719	\N	\N	\N	f
8fc93110-4a04-40d1-94c4-ff9da1b59353	CUST-34397C6D	testuser_7c8ce1@example.com	\N	customer	t	f	2026-08-16 14:55:37.510846	\N	\N	\N	f
802000c3-595a-4b4b-b853-50b4552a7f9c	CUST-BF2AFB6A	testuser_6e8455@example.com	\N	customer	t	f	2026-08-16 15:04:31.749344	\N	\N	\N	f
18ff6235-911a-473a-860c-e0bcdf972582	CUST-D9EF5E87	testuser_374e94@example.com	\N	customer	t	f	2026-08-16 18:44:50.111916	\N	\N	\N	f
5c531f9d-c62a-406f-8e63-1e376d830e62	CUST-9B336595	testuser_a1fea1@example.com	\N	customer	t	f	2026-08-16 18:45:25.465343	\N	\N	\N	f
ebd95344-744e-44dc-8f0b-d8c442a641aa	CUST-3124800E	testuser_49c171@example.com	\N	customer	t	f	2026-08-16 18:49:11.791623	\N	\N	\N	f
57c98237-c797-42e5-8a6d-867e51fe7c3d	CUST-90EDDB12	testuser_6de0ce@example.com	\N	customer	t	f	2026-08-16 18:50:17.031388	\N	\N	\N	f
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: client_invitations client_invitations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_invitations
    ADD CONSTRAINT client_invitations_pkey PRIMARY KEY (id);


--
-- Name: complaint_address complaint_address_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaint_address
    ADD CONSTRAINT complaint_address_pkey PRIMARY KEY (id);


--
-- Name: complaint_ai_analysis complaint_ai_analysis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaint_ai_analysis
    ADD CONSTRAINT complaint_ai_analysis_pkey PRIMARY KEY (id);


--
-- Name: complaint_priority_scores complaint_priority_scores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaint_priority_scores
    ADD CONSTRAINT complaint_priority_scores_pkey PRIMARY KEY (id);


--
-- Name: complaints complaints_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_pkey PRIMARY KEY (id);


--
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (id);


--
-- Name: profiles profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (id);


--
-- Name: profiles profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_user_id_key UNIQUE (user_id);


--
-- Name: service_details service_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.service_details
    ADD CONSTRAINT service_details_pkey PRIMARY KEY (id);


--
-- Name: service_details service_details_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.service_details
    ADD CONSTRAINT service_details_user_id_key UNIQUE (user_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_client_invitations_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_client_invitations_email ON public.client_invitations USING btree (email);


--
-- Name: ix_client_invitations_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_client_invitations_id ON public.client_invitations USING btree (id);


--
-- Name: ix_client_invitations_token; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_client_invitations_token ON public.client_invitations USING btree (token);


--
-- Name: ix_complaint_address_complaint_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_complaint_address_complaint_id ON public.complaint_address USING btree (complaint_id);


--
-- Name: ix_complaint_address_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_complaint_address_id ON public.complaint_address USING btree (id);


--
-- Name: ix_complaint_ai_analysis_complaint_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_complaint_ai_analysis_complaint_id ON public.complaint_ai_analysis USING btree (complaint_id);


--
-- Name: ix_complaint_ai_analysis_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_complaint_ai_analysis_id ON public.complaint_ai_analysis USING btree (id);


--
-- Name: ix_complaint_priority_scores_complaint_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_complaint_priority_scores_complaint_id ON public.complaint_priority_scores USING btree (complaint_id);


--
-- Name: ix_complaint_priority_scores_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_complaint_priority_scores_id ON public.complaint_priority_scores USING btree (id);


--
-- Name: ix_complaints_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_complaints_id ON public.complaints USING btree (id);


--
-- Name: ix_complaints_ticket_number; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_complaints_ticket_number ON public.complaints USING btree (ticket_number);


--
-- Name: ix_departments_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_departments_id ON public.departments USING btree (id);


--
-- Name: ix_departments_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_departments_name ON public.departments USING btree (name);


--
-- Name: ix_profiles_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_profiles_id ON public.profiles USING btree (id);


--
-- Name: ix_service_details_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_service_details_id ON public.service_details USING btree (id);


--
-- Name: ix_users_customer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_customer_id ON public.users USING btree (customer_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: client_invitations client_invitations_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_invitations
    ADD CONSTRAINT client_invitations_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id) ON DELETE CASCADE;


--
-- Name: complaint_address complaint_address_complaint_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaint_address
    ADD CONSTRAINT complaint_address_complaint_id_fkey FOREIGN KEY (complaint_id) REFERENCES public.complaints(id) ON DELETE CASCADE;


--
-- Name: complaint_ai_analysis complaint_ai_analysis_complaint_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaint_ai_analysis
    ADD CONSTRAINT complaint_ai_analysis_complaint_id_fkey FOREIGN KEY (complaint_id) REFERENCES public.complaints(id) ON DELETE CASCADE;


--
-- Name: complaint_priority_scores complaint_priority_scores_complaint_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaint_priority_scores
    ADD CONSTRAINT complaint_priority_scores_complaint_id_fkey FOREIGN KEY (complaint_id) REFERENCES public.complaints(id) ON DELETE CASCADE;


--
-- Name: complaints complaints_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: profiles profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: service_details service_details_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.service_details
    ADD CONSTRAINT service_details_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: users users_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

