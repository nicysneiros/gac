/*Script SQL - Cliente*/
BEGIN;
CREATE TABLE "Endereco" (
    "id" serial NOT NULL PRIMARY KEY,
    "logradouro" text NOT NULL,
    "complemento" text NOT NULL,
    "bairro" text NOT NULL,
    "cidade" text NOT NULL,
    "cep" text NOT NULL
)
;
CREATE TABLE "Cliente" (
    "id" varchar(15) NOT NULL PRIMARY KEY,
    "nome" text NOT NULL,
    "email" varchar(75) NOT NULL,
    "ID_Endereco" integer NOT NULL REFERENCES "Endereco" ("id") DEFERRABLE INITIALLY DEFERRED,
    "telResidencial" text NOT NULL,
    "telCelular" text NOT NULL,
    "juridico" boolean NOT NULL
)
;
CREATE INDEX "Cliente_id_like" ON "Cliente" ("id" varchar_pattern_ops);
CREATE INDEX "Cliente_ID_Endereco" ON "Cliente" ("ID_Endereco");

COMMIT;

/*Script SQL - Pedido*/
BEGIN;
CREATE TABLE "Servico" (
    "id" serial NOT NULL PRIMARY KEY,
    "valor" double precision NOT NULL,
    "descricao" text,
    "ID_Cliente" varchar(15) REFERENCES "Cliente" ("id") DEFERRABLE INITIALLY DEFERRED,
    "data" date
)
;
CREATE TABLE "Pedido" (
    "servico_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "Servico" ("id") DEFERRABLE INITIALLY DEFERRED,
    "prazo" date NOT NULL,
    "desenho" varchar(100)
)
;
CREATE TABLE "Corporativo" (
    "pedido_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "Pedido" ("servico_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "qtd_P" integer NOT NULL,
    "qtd_M" integer NOT NULL,
    "qtd_G" integer NOT NULL
)
;
CREATE TABLE "Personalizado" (
    "pedido_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "Pedido" ("servico_ptr_id") DEFERRABLE INITIALLY DEFERRED,
    "altura" text NOT NULL,
    "largura" text NOT NULL
)
;
CREATE TABLE "Despesa" (
    "id" serial NOT NULL PRIMARY KEY,
    "valor" double precision NOT NULL,
    "fornecedor" text NOT NULL,
    "descricao" text NOT NULL,
    "ID_Servico" integer NOT NULL REFERENCES "Servico" ("id") DEFERRABLE INITIALLY DEFERRED,
    "data" date NOT NULL
)
;
CREATE INDEX "Servico_ID_Cliente" ON "Servico" ("ID_Cliente");
CREATE INDEX "Servico_ID_Cliente_like" ON "Servico" ("ID_Cliente" varchar_pattern_ops);
CREATE INDEX "Despesa_ID_Servico" ON "Despesa" ("ID_Servico");

COMMIT;

/*Script SQL - Produto*/
BEGIN;
CREATE TABLE "Produto" (
    "servico_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "Servico" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tamanho" text NOT NULL,
    "categoria" text NOT NULL,
    "foto" varchar(100),
    "titulo" text NOT NULL,
    "portfolio" boolean NOT NULL
)
;

COMMIT;

