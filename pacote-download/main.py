import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

class GerenciadorDeProdutos:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Gerenciador de Produtos")
        self.janela.geometry("800x600")

        self.produtos = {}

        self.abas = ttk.Notebook(janela)
        self.abas.pack(fill='both', expand=True, padx=10, pady=10)


        self.criar_aba("Adicionar Produto", self.setup_aba_adicionar)
        self.criar_aba("Listar Produtos", self.setup_aba_listar)
        self.criar_aba("Remover Produto", self.setup_aba_remover)
        self.criar_aba("Atualizar Produto", self.setup_aba_atualizar)
        self.criar_aba("Remover Quantidade", self.setup_aba_remover_quantidade)
        self.criar_aba("Adicionar Quantidade", self.setup_aba_adicionar_quantidade)

    def criar_aba(self, titulo, configuracao):
        aba = ttk.Frame(self.abas)
        self.abas.add(aba, text=titulo)
        configuracao(aba)

    def setup_aba_adicionar(self, aba):
        self.entrada_codigo = self.criar_campo(aba, "Código:", 0)
        self.entrada_nome = self.criar_campo(aba, "Nome:", 1)
        self.entrada_preco = self.criar_campo(aba, "Preço:", 2)
        self.entrada_quantidade = self.criar_campo(aba, "Quantidade:", 3)

        ttk.Button(aba, text="Adicionar", command=self.adicionar_produto).grid(row=4, column=0, columnspan=2, pady=10)

    def setup_aba_listar(self, aba):
        self.area_texto = ScrolledText(aba, width=70, height=20)
        self.area_texto.pack(padx=10, pady=10)
        ttk.Button(aba, text="Atualizar Lista", command=self.listar_produtos).pack(pady=10)

    def setup_aba_remover(self, aba):
        self.entrada_remover = self.criar_campo(aba, "Código do Produto:", 0)
        ttk.Button(aba, text="Remover", command=self.remover_produto).grid(row=1, column=0, columnspan=2, pady=10)

    def setup_aba_atualizar(self, aba):
        self.entrada_codigo_upd = self.criar_campo(aba, "Código:", 0)
        self.entrada_nome_upd = self.criar_campo(aba, "Novo Nome:", 1)
        self.entrada_preco_upd = self.criar_campo(aba, "Novo Preço:", 2)
        self.entrada_quantidade_upd = self.criar_campo(aba, "Nova Quantidade:", 3)

        ttk.Button(aba, text="Atualizar", command=self.atualizar_produto).grid(row=4, column=0, columnspan=2, pady=10)

    def setup_aba_remover_quantidade(self, aba):
        self.entrada_cod_rem_qtd = self.criar_campo(aba, "Código:", 0)
        self.entrada_rem_qtd = self.criar_campo(aba, "Quantidade a Remover:", 1)

        ttk.Button(aba, text="Remover Quantidade", command=self.remover_quantidade).grid(row=2, column=0, columnspan=2, pady=10)

    def setup_aba_adicionar_quantidade(self, aba):
        self.entrada_cod_add_qtd = self.criar_campo(aba, "Código:", 0)
        self.entrada_add_qtd = self.criar_campo(aba, "Quantidade a Adicionar:", 1)

        ttk.Button(aba, text="Adicionar Quantidade", command=self.adicionar_quantidade).grid(row=2, column=0, columnspan=2, pady=10)

    def criar_campo(self, frame, texto, linha):
        ttk.Label(frame, text=texto).grid(row=linha, column=0, padx=10, pady=5)
        entrada = ttk.Entry(frame)
        entrada.grid(row=linha, column=1, padx=10, pady=5)
        return entrada

    def adicionar_produto(self):
        try:
            codigo = self.entrada_codigo.get()
            nome = self.entrada_nome.get()
            preco = float(self.entrada_preco.get())
            quantidade = int(self.entrada_quantidade.get())

            self.produtos[codigo] = {
                "Nome": nome,
                "Preço": preco,
                "Quantidade": quantidade
            }

            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
            self.limpar_campos([self.entrada_codigo, self.entrada_nome, self.entrada_preco, self.entrada_quantidade])
        except ValueError:
            messagebox.showerror("Erro", "Verifique os campos de preço e quantidade.")

    def listar_produtos(self):
        self.area_texto.delete(1.0, tk.END)
        if not self.produtos:
            self.area_texto.insert(tk.END, "Nenhum produto cadastrado.\n")
        else:
            for cod, dados in self.produtos.items():
                self.area_texto.insert(tk.END, f"Código: {cod}\n")
                for chave, valor in dados.items():
                    self.area_texto.insert(tk.END, f"  {chave}: {valor}\n")
                self.area_texto.insert(tk.END, "\n")

    def remover_produto(self):
        codigo = self.entrada_remover.get()
        if codigo in self.produtos:
            del self.produtos[codigo]
            messagebox.showinfo("Sucesso", f"Produto {codigo} removido.")
            self.entrada_remover.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")

    def atualizar_produto(self):
        codigo = self.entrada_codigo_upd.get()
        if codigo in self.produtos:
            try:
                nome = self.entrada_nome_upd.get()
                preco = float(self.entrada_preco_upd.get())
                quantidade = int(self.entrada_quantidade_upd.get())
                self.produtos[codigo] = {"Nome": nome, "Preço": preco, "Quantidade": quantidade}
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
                self.limpar_campos([self.entrada_codigo_upd, self.entrada_nome_upd, self.entrada_preco_upd, self.entrada_quantidade_upd])
            except ValueError:
                messagebox.showerror("Erro", "Verifique os campos de preço e quantidade.")
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")

    def remover_quantidade(self):
        codigo = self.entrada_cod_rem_qtd.get()
        if codigo in self.produtos:
            try:
                qtd = int(self.entrada_rem_qtd.get())
                atual = self.produtos[codigo]["Quantidade"]
                if qtd <= atual:
                    self.produtos[codigo]["Quantidade"] -= qtd
                    messagebox.showinfo("Sucesso", f"Removido {qtd} unidade(s).")
                    self.limpar_campos([self.entrada_cod_rem_qtd, self.entrada_rem_qtd])
                else:
                    messagebox.showerror("Erro", f"Estoque insuficiente. Atual: {atual}")
            except ValueError:
                messagebox.showerror("Erro", "Quantidade inválida.")
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")

    def adicionar_quantidade(self):
        codigo = self.entrada_cod_add_qtd.get()
        if codigo in self.produtos:
            try:
                qtd = int(self.entrada_add_qtd.get())
                if qtd > 0:
                    self.produtos[codigo]["Quantidade"] += qtd
                    messagebox.showinfo("Sucesso", f"Adicionado {qtd} unidade(s).")
                    self.limpar_campos([self.entrada_cod_add_qtd, self.entrada_add_qtd])
                else:
                    messagebox.showerror("Erro", "Quantidade deve ser positiva.")
            except ValueError:
                messagebox.showerror("Erro", "Quantidade inválida.")
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")

    def limpar_campos(self, campos):
        for campo in campos:
            campo.delete(0, tk.END)

if __name__ == "__main__":
    janela = tk.Tk()
    app = GerenciadorDeProdutos(janela)
    janela.mainloop()
