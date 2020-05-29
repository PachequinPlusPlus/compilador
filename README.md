# Compilador
Proyecto final de compiladores

El lenguaje PPCDSALVC (Python Programming Compiler Daniel SAmuel Luis Vazquez Cantu) es un lenguaje para que las personas que son nuevas al concepto de Objetos y a la programación imperativa puedan empezar a aprender. Se necesita tener instalado ANTLR4 para poder compilar el programa

Para poder correr usar nuestro compilador se tiene que usar el comando

<pre><code>
python3 PPCDSALVC.py --programa file_path --quad_file archivo.ppc --quads path_to_save [--help | -h | --logs log_file | --show_quads | --show_logs ]
</code></pre>

Las flags obligatorias que le tienes que mandar al compilador para que compile el programa con las del nombre del programa, el nombre del archivo a generar y el directorio donde guardar el código intermedio generado, se puede utilizar ./ para usar el path actual.

Las flags opcionales son las que creamos para ayudarnos en el proceso de desarrollo, donde --logs te permite especificar un archivo donde guardar los logs del compilador. --show_quads y --show_logs te permite imprimir directamente en la compilación la información de cuadruplos y de logs que genera nuestro compilador. --help te permite ver la descripción de las flags.

# Maquina Virtual

Para correr la maquina virtual se puede usar el comando

<pre><code>
python3 maquinaVirtual.py compiled_file.ppc
</code></pre>

En la maquina virtual solo especificamos el archivo que se genero por el compilaor para poder correr el programa.


# Ejemlos

Estos son algunos de los ejemplos de programas que se pueden crear en nuestro lenguaje PPCDSALVC

Fibonacci
<pre><code>
program fiboIter;

func int fibonacciIt(int n){
    var {
      int retorno, i, num1, num2;
      int fibo1, fibo2;
    }
    if (n == 0) {
      retorno = 0;
    } elseif(n == 1 || n == 2) {
      retorno = 1;
    }
    num1 = 0;
    num2 = 1;
    for(i = 2; i <= n; i = i + 1) {
      retorno = num1 + num2;
      num1 = num2;
      num2 = retorno;
    }
    return retorno;
}

main {
    var{
        int n;
    }
    n = 10;
    print(fibonacciIt(n), '\n');
}

</code></pre>

Fact
<pre><code>
program factorial;

func int factorial(int n) {
  var {
    int i, retorno;
  }
  if (n == 0) {
    retorno = 0;
  } else {
    retorno = 1;
    for (i = 2; i <= n; i = i+1) {
      retorno = retorno*i;
    }
  }
  return retorno;
}

main {
  var {
    int n;
  }
  n = 10;
  print(factorial(10), '\n');
}

</code></pre>

Merge Sort
<pre><code>
program mergeSort;
var{
    int arreglo[55], n, i;
}

func void mergeSort(int l, int r) {
    var {
        int aux[55], m, left, right, k;
    }
    if(l < r && l >= 0 && r < n){
        m = (l + r) / 2;
        mergeSort(l, m);
        mergeSort(m+1, r);

        left = l;
        right = m + 1;
        k = 0;
        while(left <= m && right <= r){
           if( arreglo[left] <= arreglo[right] ){
            aux[k] = arreglo[left]; 
            left = left + 1;
           }else{
            aux[k] = arreglo[right];
            right = right + 1;
           }
           k = k + 1;
        }

        while(left <= m){
            aux[k] = arreglo[left]; 
            left = left + 1;
            k = k + 1;
        }

        while(right <= r){
            aux[k] = arreglo[right];
            right = right + 1;
            k = k + 1;    
        }
        for(i = 0; i < k; i = i + 1){
            arreglo[i + l] = aux[i];
        }
    }}

main {
  n = 55;
  print(n, '\n');
  for(i = 0; i < n; i = i + 1){
    arreglo[i] = n - i;
  }

  mergeSort(0, n-1);

  for(i = 0; i < n; i = i + 1){
    print(arreglo[i], ' ');
  }
    print('\n');
}
</code></pre>
