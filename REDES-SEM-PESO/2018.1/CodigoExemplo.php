ANEXO A – CÓDIGO REDE WISARD
<?php
// *** MAIN CLASS *** //
class Wisard {
	var $discriminators;
	//Construtor
	public function Wisard(){
		$this->discriminators = new ArrayObject();//vetor de discriminadores
	}
	public function addDiscriminator($discriminator){
		$this->discriminators->append($discriminator);//"gruda" novo discriminador na lista de discriminadores antiga
	}
	public function delDiscriminator($discriminator){//???
		//$this->discriminators->
	}
	public function showDiscriminators(){
		print "There is a total of: ".$this->discriminators->count()." discriminators"; //total de discriminadores
		for($i=0;$i<$this->discriminators->count();$i++){
			print "<br/>".$this->discriminators[$i]->getClassName();//nome dos discriminadores
		}
	}
	public function show(){
		print_r($this->discriminators);
	}
	public function detect($pattern){
		$best_score = 0;
		$second_score =0;
		$winner_class ="";
		for($i=0;$i<$this->discriminators->count();$i++){			
			$points = $this->discriminators[$i]->check($pattern);
			 if($points>$best_score){
			 	$second_score = $best_score;
			 	$best_score = $points;
			 	$winner_class = $this->discriminators[$i]->getClassName();
			 }
		}
		return "Winner class:".$winner_class." com score :".$best_score;//mostra padrao mais compatível
	}
}
// *** DISCRIMINATOR *** //
class Discriminator{
	var $class_name = "";//inicializa atributos
	var $neurons;
	var $neurons_bits;
	var $training = 0;	//marca qntos elementos foram usados para treinar
	var $knowledge;		//pardao armazenado
	//Construtor
	public function Discriminator($class_name,$neurons,$neurons_bits){
		$this->class_name    = $class_name;		//nome da discriminador
		$this->neurons       = $neurons;		//numero de neuronios(rams)
		$this->neurons_bits  = $neurons_bits;	//numero de bits em cada neuronio
		//Set of neurons for each discriminator
		$this->knowledge = new ArrayObject();
		for($i=0;$i<$this->neurons;$i++){
			$this->knowledge[$i] = new RAM($this->neurons_bits);
		}
	}
	public function training($training_set){
		$this->training++;
		for($i=0;$i<$this->knowledge->count();$i++){
			$this->knowledge[$i]->activate_neurons($training_set[$i]);
		}
	}
	public function check($pattern){
		$neurons_activated =0;
		for($i=0;$i<$this->knowledge->count();$i++){//*****// VARRE DE 1 EM 1 //*****//
//		for($i=0;$i<$size;$i++){//*****// VARRE DE 1 EM 1 //*****//	
			$neurons_activated = $neurons_activated + $this->knowledge[$i]->check($pattern[$i]);
		}		
		return $neurons_activated;
	}
	public function clear(){
		for($i=0;$i<$this->neurons;$i++){
			$this->knowledge[$i]->clear();
		}
	}
	public function getClassName(){
		return $this->class_name;
	}
	public function show(){
		print "<br/>Class: ".$this->class_name."<br/>";
		print "<br/>Neurons: ".$this->neurons." with: ".$this->neurons_bits." bits each!<br/>";
		print "<pre>";
		print_r($this->knowledge);
		print "</pre>";
	}	
}
// *** RAM CLASS *** //
	class RAM {
		var $bits;
		var $ram;
		//Construtor
		public function RAM($b){
			$this->bits = $b;
			$this->ram  = new ArrayObject();
			for($i=0;$i<$this->bits;$i++){
				$this->ram[$i]=false; //Atribui '0' em tudo
			}
		}
		public function clear(){
			for($i=0;$i<$this->bits;$i++){//limpa RAM
				$this->ram[$i]=false;
			}
		}
		public function neurons_activated(){
			$count = 0;
			for($i=0;$i<$this->ram->count();$i++){//percorre todos os bits
				if($this->ram[$i]==true){//conta todos os que deram verdadeiro
					$count++;
				}
			}
			return $count;
		}
		public function check($pattern){ 
			for($i=0;$i< $this->bits;$i++){ //percorre todos os bits
				if(($this->ram[$i]==false) && ($pattern[$i]==true)){//conta os que deram verdadeiros iguais "matches"
					return false;
				}
			}
			return true;
		}
		
		public function activate_neurons($pattern){
			for($i=0;$i< $this->bits;$i++){//percorre todos os bits
				if(($this->ram[$i]==false) && ($pattern[$i]==true)){//se na ram for falso e no padrao verdadeiro
					$this->activate_neuron($i);//ativa
				}
			}
		}
		public function activate_neuron($i){// ??? nao entendi o raio da funcao...mas ativa...rsr
			try{
				if($this->ram->offsetExists($i)){
					$this->ram[$i]=!$this->ram[$i];
				}				
			}
			catch(Exception $e){
				echo "<h1>Erro</h1>";
				echo $e->getMessage();
			}
		}
		public function show(){
			print  ("<br/>RAM with".$this->bits." bits<br/>");
			print ("<pre>");
			print_r($this->ram);
			print ("</pre>");

		}
	}
?> 
