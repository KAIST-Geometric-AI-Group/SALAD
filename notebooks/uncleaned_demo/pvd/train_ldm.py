# < Seungwoo >
# Temporarily re-locate files to avoid errors during import.
####
import jutils

import hydra
import pytorch_lightning as pl
# import jutils
####

@hydra.main(config_path="configs", config_name="train.yaml")
def main(config):
    pl.seed_everything(63)

    #### < Seungwoo > 
    # To make W&B sweep work, need to explicitly initialize W&B
    # Remove this line after finishing hyperparameter search
    # import wandb
    # wandb.init(settings=wandb.Settings(start_method="fork") )
    ####

    jutils.sysutil.print_config(config, ("callbacks", "logger", "paths", "experiment", "debug", "data", "trainer", "model"))
    model = hydra.utils.instantiate(config.model, _recursive_=True)

    callbacks = []
    if config.get("callbacks"):
        for cb_name, cb_conf in config.callbacks.items():
            if config.get("debug") and cb_name == "model_checkpoint":
                continue
            # if cb_name == "lr_monitor":
                # continue
            callbacks.append(hydra.utils.instantiate(cb_conf))

    logger = []
    if config.get("logger"):
        for lg_name, lg_conf in config.logger.items():
            if config.get("debug") and lg_name == "wandb":
                continue
            logger.append(hydra.utils.instantiate(lg_conf))
    trainer = hydra.utils.instantiate(
        config.trainer,
        callbacks=callbacks,
        logger=logger if len(logger) != 0 else False,
        # logger=False,
        _convert_="partial",
        log_every_n_steps=200,
        resume_from_checkpoint=config.resume_from_checkpoint
    )

    trainer.fit(model)

if __name__ == "__main__":
    main()
